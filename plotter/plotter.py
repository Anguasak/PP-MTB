'''
Minimal script to plot simulation results from PSCAD and PowerFactory.
'''
from __future__ import annotations
from os import listdir, makedirs
from os.path import join, split, splitext, exists
import re
import pandas as pd
from plotly.subplots import make_subplots #type: ignore
import plotly.graph_objects as go #type: ignore
from typing import List, Dict, Union, Tuple, Set
import sampling_functions
from down_sampling_method import DownSamplingMethod
from threading import Thread, Lock
import time
import sys
from math import ceil
from collections import defaultdict
import plot_cursor_functions
from read_configs import ReadConfig, readFigureSetup, readRankSetup
from Figure import Figure
from Result import ResultType, Result
from Case import Case
from Rank import Rank


try:
    LOG_FILE = open('plotter.log', 'w')
except:
    print('Failed to open log file. Logging to file disabled.')
    LOG_FILE = None #type: ignore

gLock = Lock()

def print(*args): #type: ignore
    '''
    Overwrites the print function to also write to a log file.
    '''
    gLock.acquire()
    outputString = ''.join(map(str, args)) + '\n' #type: ignore
    sys.stdout.write(outputString)
    if LOG_FILE:
        try:
            LOG_FILE.write(outputString)
            LOG_FILE.flush()
        except:
            pass
    gLock.release()


def idFile(filePath: str) -> Tuple[Union[ResultType, None], Union[int, None], Union[str, None], Union[str, None], Union[str, None]]:
    '''
    Identifies the type (EMT or RMS), root and case id of a given file. If the file is not recognized, a none tuple is returned.
    '''
    path, fileName = split(filePath)
    match = re.match(r'^(\w+?)_([0-9]+).(inf|csv)$', fileName.lower())
    if match:
        rank = int(match.group(2))
        projectName = match.group(1)
        bulkName = join(path, match.group(1))
        fullpath = filePath
        with open(filePath, 'r') as file:
            firstLine = file.readline()
            if match.group(3) == 'inf' and firstLine.startswith('PGB(1)'):
                fileType = ResultType.EMT
                return (fileType, rank, projectName, bulkName, fullpath)
            elif match.group(3) == 'csv':
                secondLine = file.readline()
                if secondLine.startswith(r'"b:tnow in s"'):
                    fileType = ResultType.RMS
                    return (fileType, rank, projectName, bulkName, fullpath)
    return (None, None, None, None, None)

def mapResultFiles(config : ReadConfig) -> Dict[int, List[Result]]:
    '''
    Goes through all files in the given directories and maps them to a dictionary of cases.
    '''
    files : List[Tuple[str, str]] = list()
    for dir_ in config.simDataDirs:
        for file_ in listdir(dir_[1]):
            files.append((dir_[0], join(dir_[1], file_)))

    results : Dict[int, List[Result]] = dict()

    for file in files:
        group = file[0]
        fullpath = file[1]
        typ, rank, projectName, bulkName, fullpath = idFile(fullpath)

        if typ is None:
            continue
        assert rank is not None
        assert projectName is not None
        assert bulkName is not None
        assert fullpath is not None

        newResult = Result(typ, rank, projectName, bulkName, fullpath, group)

        if rank in results.keys():
            results[rank].append(newResult)
        else:
            results[rank] = [newResult]

    return results

def emtColumns(infFilePath : str) -> Dict[int, str]:
    '''
    Reads EMT result columns from the given inf file and returns a dictionary with the column number as key and the column name as value.
    '''
    columns : Dict[int, str] = dict()
    with open(infFilePath, 'r') as file:
        for line in file: 
            rem = re.match(r'^PGB\(([0-9]+)\) +Output +Desc="(\w+)" +Group="(\w+)" +Max=([0-9\-\.]+) +Min=([0-9\-\.]+) +Units="(\w*)" *$', line)
            if rem:
                columns[int(rem.group(1))] = rem.group(2) 
    return columns

def loadEMT(infFile : str) -> pd.DataFrame:
    '''
    Load EMT results from a collection of csv files defined by the given inf file. Returns a dataframe with index 'time'.
    '''
    folder, filename = split(infFile)
    filename, fileext = splitext(filename)
 
    assert fileext.lower() == '.inf'

    adjFiles = listdir(folder)
    csvMap : Dict[int, str]= dict()
    pat = re.compile(r'^' + filename.lower() + r'(?:_([0-9]+))?.csv$')

    for file in adjFiles:
        rem = re.match(pat, file.lower())
        if rem:
            if rem.group(1) is None:
                id = -1
            else:
                id = int(rem.group(1))
            csvMap[id] = join(folder, file)
    csvMaps = list(csvMap.keys())
    csvMaps.sort()
    
    df = pd.DataFrame()
    firstFile = True
    loadedColumns = 0
    for map in csvMaps:
        dfMap = pd.read_csv(csvMap[map], skiprows = 1, header = None) #type: ignore
        if not firstFile:
            dfMap = dfMap.iloc[: , 1:]
        else:
            firstFile = False
        dfMap.columns = list(range(loadedColumns, loadedColumns + len(dfMap.columns)))
        loadedColumns = loadedColumns + len(dfMap.columns)
        df = pd.concat([df, dfMap], axis=1) #type: ignore

    columns = emtColumns(infFile)
    columns[0] = 'time'
    df = df[columns.keys()]
    df.rename(columns, inplace=True, axis=1)
    print(f"Loaded {infFile}, length = {df['time'].iloc[-1]}s") #type: ignore   
    return df

def colorMap(results: Dict[int, List[Result]]) -> Dict[str, List[str]]:
    '''
    Select colors for the given projects. Return a dictionary with the project name as key and a list of colors as value.
    '''
    colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#000000']
    
    projects : Set[str] = set()

    for rank in results.keys():
        for result in results[rank]:
            projects.add(result.shorthand)

    cMap : Dict[str, List[str]] = dict()

    if len(list(projects)) > 2:
        i = 0
        for p in list(projects):
            cMap[p] = [colors[i % len(colors)]] * 3
            i += 1
        return cMap
    else:
        i = 0
        for p in list(projects):
            cMap[p] = colors[i:i+3]
            i += 3
    return cMap


def addCursors(htmlPlots: List[go.Figure],
               typ: ResultType,
               data: pd.DataFrame,
               rankDict: List[Rank],
               pfFlatTIme: float,
               pscadInitTime: float,
               rank: int,
               nColumns: int):
    rank_settings = [i for i in rankDict if i.id == rank]
    if len(rank_settings) == 0:
        return list()

    signalKey = typ.name.lower()

    # Initialize subplot positions
    fi = -1  # Start index from -1 as it is incremented before use

    # Loop through rank settings
    for rank_setting in rank_settings:
        rawSigNames = getattr(rank_setting, f'{signalKey}_signals')
        threshold = getattr(rank_setting, 'cursor_time_ranges')
        # Increment plot index
        fi += 1

        if len(rawSigNames) == 0:
            continue

        # Update subplot row and column positions based on fi
        rowPos = (fi // nColumns) + 1
        colPos = (fi % nColumns) + 1

        # Select the correct plot
        plot = htmlPlots[fi] if nColumns == 1 else htmlPlots[0]

        x = []
        y = []

        for rawSigName in rawSigNames:
            if typ == ResultType.RMS:
                # Remove hash and split signal name
                while rawSigName.startswith('#'):
                    rawSigName = rawSigName[1:]
                splitSigName = rawSigName.split('\\')

                if len(splitSigName) == 2:
                    sigColumn = ('##' + splitSigName[0], splitSigName[1])
                else:
                    sigColumn = rawSigName
            else:
                sigColumn = rawSigName

            # Determine the time column and offset based on the type
            timeColName = 'time' if typ == ResultType.EMT else data.columns[0]
            timeoffset = pfFlatTIme if typ == ResultType.RMS else pscadInitTime

            if sigColumn in data.columns:
                # Get the signal data and time values
                x.extend(data[timeColName] - timeoffset)  # type: ignore
                y.extend(data[sigColumn])  # type: ignore

        # Filter the data based on the threshold
        if len(y) != 0:
            x = pd.Series(x)
            y = pd.Series(y)

            if len(threshold) > 0:
                assert len(threshold) <= 2
                mask = (x >= threshold[0]) & (x < threshold[1]) if len(threshold) == 2 else (x >= threshold[0])
                y_filtered = y[mask]
                x_filtered = x[mask]
            else:
                y_filtered = y
                x_filtered = x

            plot_cursor_functions.add_annotations_subplot(plot, x_filtered, y_filtered, rowPos, colPos)

        else:
            plot.add_trace(go.Scatter(x=[], y=[], mode='lines', name='No Data'), row=rowPos, col=colPos)
            # Keep the title for empty plot
            # Add an annotation to indicate no data
            plot.update_xaxes(visible=False, row=rowPos, col=colPos)
            plot.update_yaxes(visible=False, row=rowPos, col=colPos)

    return htmlPlots  # Return updated plots



def addResults(    plots : List[go.Figure],
                   typ: ResultType,
                   data: pd.DataFrame,
                   figures: List[Figure],
                   resultName: str,
                   file: str, #Only for error messages
                   colors: Dict[str, List[str]],
                   nColumns: int,
                   pfFlatTIme : float,
                   pscadInitTime : float) -> None:
    '''
    Add result to plot.
    '''

    assert nColumns > 0

    if nColumns > 1:    
        plotlyFigure = plots[0]
    else:
         assert len(plots) == len(figures)

    rowPos = 1
    colPos = 1
    fi = -1
    for figure in figures:
        fi += 1
        
        if nColumns == 1:
            plotlyFigure = plots[fi]
        else:
            rowPos = (fi // nColumns) + 1
            colPos = (fi % nColumns) + 1
            
        downsampling_method = figure.down_sampling_method
        traces = 0
        for sig in range(1,4):
            signalKey = typ.name.lower()
            rawSigName : str = getattr(figure, f'{signalKey}_signal_{sig}')
            
            if typ == ResultType.RMS:
                while rawSigName.startswith('#'):
                    rawSigName = rawSigName[1:]
                splitSigName = rawSigName.split('\\')

                if len(splitSigName) == 2:
                    sigColumn = ('##' + splitSigName[0], splitSigName[1])
                else:
                    sigColumn = rawSigName
            else:
                sigColumn = rawSigName

            displayName = f'{resultName}:{rawSigName.split(" ")[0]}'

            timeColName = 'time' if typ == ResultType.EMT else data.columns[0]
            timeoffset = pfFlatTIme if typ == ResultType.RMS else pscadInitTime

            if sigColumn in data.columns:
                x_value = data[timeColName] - timeoffset #type: ignore
                y_value = data[sigColumn] #type: ignore
                if downsampling_method == DownSamplingMethod.GRADIENT:
                    x_value, y_value = sampling_functions.downsample_based_on_gradient(x_value, y_value, figure.gradient_threshold) #type: ignore
                elif downsampling_method == DownSamplingMethod.AMOUNT:
                    x_value, y_value = sampling_functions.down_sample(x_value, y_value) #type: ignore

                plotlyFigure.add_trace( #type: ignore
                    go.Scatter(
                        x=x_value,
                        y=y_value,
                        line_color=colors[resultName][traces],
                        name=displayName,
                        legendgroup=resultName if nColumns > 1 else displayName,
                        showlegend=True
                    ),
                    row=rowPos, col=colPos
                )
                #plot_cursor_functions.add_annotations(x_value, y_value, plotlyFigure)
                traces += 1
            elif sigColumn != '':
                print(f'Signal "{rawSigName}" not recognized in resultfile: {file}')
                plotlyFigure.add_trace( #type: ignore
                    go.Scatter(
                    x=None,
                    y=None,
                    line_color=colors[resultName][traces], 
                    name=f'{displayName} (Unknown)',
                    legendgroup=resultName if nColumns > 1 else displayName,
                    showlegend=True
                ),
                row=rowPos, col=colPos
                )
                traces += 1               
        
        plotlyFigure.update_xaxes( #type: ignore
            title_text='Time[s]',  
            row=rowPos, col=colPos
        )
        if nColumns == 1:
            yaxisTitle = f'[{figure.units}]'
        else:
            yaxisTitle = f'{figure.title}[{figure.units}]'

        plotlyFigure.update_yaxes( #type: ignore
            title_text=yaxisTitle ,  
            row=rowPos, col=colPos
        )

def drawPlot( rank : int,
                resultDict : Dict[int, List[Result]],
                figureDict : Dict[int, List[Figure]],
                caseDict : Dict[int, str],
                colorMap : Dict[str, List[str]],
                rankDict: List[Rank],
                config : ReadConfig):
    
    '''
    Draws plots for html and static image export.    
    '''

    print(f'Drawing plot for rank {rank}.')

    resultList = resultDict.get(rank, [])
    figureList = figureDict[rank]
    figureListCursor = [i for i in rankDict if i.id == rank]

    if resultList == [] or figureList == []:
        return

    figurePath = join(config.resultsDir, str(rank))

    htmlPlots : List[go.Figure] = list()
    imagePlots : List[go.Figure] = list()
    htmlPlotsCursors : List[go.Figure] = list()

    columnNr = setupPlotLayout(caseDict, config, figureList, htmlPlots, imagePlots, rank)
    if len(figureListCursor) > 0:
        setupPlotLayout(caseDict, config, figureListCursor, htmlPlotsCursors, imagePlots, rank, True)
    for result in resultList:
        if result.typ == ResultType.RMS:
            resultData : pd.DataFrame = pd.read_csv(result.fullpath, sep=';',decimal=',',header=[0,1]) #type: ignore
        elif result.typ == ResultType.EMT:
            resultData = loadEMT(result.fullpath)
        else:
            continue
        if config.genHTML:
            addResults(htmlPlots, result.typ, resultData, figureList, result.shorthand, result.fullpath, colorMap, config.htmlColumns, config.pfFlatTIme, config.pscadInitTime)
            addCursors(htmlPlotsCursors, result.typ, resultData, rankDict, config.pfFlatTIme, config.pscadInitTime, rank, config.htmlColumns)
        if config.genImage:
            addResults(imagePlots, result.typ, resultData, figureList, result.shorthand, result.fullpath, colorMap, config.imageColumns, config.pfFlatTIme, config.pscadInitTime)
            # TODO - aax addcursors here
   
    if config.genHTML:
        create_html(htmlPlots, htmlPlotsCursors, figurePath, caseDict[rank], config)
        print(f'Exported plot for rank {rank} to {figurePath}.html')
        
    if config.genImage: 
       imagePlots[0].write_image(f'{figurePath}.{config.imageFormat}', height = 500 * ceil(len(figureList)/columnNr), width = 500*config.imageColumns) #type: ignore
       print(f'Exported plot for rank {rank} to {figurePath}.{config.imageFormat}')

    print(f'Plot for rank {rank} done.')


def setupPlotLayout(caseDict, config, figureList, htmlPlots, imagePlots, rank, showSubplotTitles = False):
    lst: List[Tuple[int, List[go.Figure]]] = []
    if config.genHTML:
        lst.append((config.htmlColumns, htmlPlots))
    if config.genImage:
        lst.append((config.imageColumns, imagePlots))

    for columnNr, plotList in lst:
        if columnNr == 1:
            for fig in figureList:
                # Create a single subplot with a title
                plotList.append(make_subplots(rows=1, cols=1, subplot_titles=(fig.title,)))  # Ensure title is set
                plotList[-1].update_layout(height=500,  # type: ignore
                                           legend=dict(
                                               orientation="h",
                                               yanchor="top",
                                               y=1.22,
                                               xanchor="left",
                                               x=0.12,
                                           ))
        elif columnNr > 1:
            if showSubplotTitles:
                num_rows = ceil(len(figureList) / columnNr)
                titles = [fig.title for fig in figureList]  # Gather titles for each subplot
                plotList.append(
                    make_subplots(rows=num_rows, cols=columnNr, subplot_titles=titles))  # Set titles for subplots
                plotList[-1].update_layout(height=500 * num_rows)  # type: ignore
            else:
                plotList.append(make_subplots(rows=ceil(len(figureList) / columnNr), cols=columnNr))
                plotList[-1].update_layout(height=500 * ceil(len(figureList) / columnNr))  # type: ignore
            if plotList == imagePlots:
                plotList[-1].update_layout(title_text=caseDict[rank])  # type: ignore
    return columnNr


def create_html(plots : List[go.Figure], cursor_plots : List[go.Figure], path : str, title : str, config : ReadConfig) -> None:
    source_list =  '<div style="text-align: left; margin-top: 1px;">'
    source_list += '<h4>Source data:</h4>'
    for group in config.simDataDirs:
        source_list += f'<p>{group[0]} = {group[1]}</p>'

    source_list += '</div>'

    html_content = create_html_plots(config, plots, title)
    html_content_cursors = create_html_plots(config, cursor_plots, title)

    full_html_content = f'''
            <html>
            <body>
                {html_content}
                {html_content_cursors}
                {source_list}
                <p><center><a href="https://github.com/Energinet-AIG/MTB" target="_blank">Generated with Energinets Model Testbench</a></center></p>
            </body>
            </html>
            '''
    
    with open(f'{path}.html', 'w') as file:
        file.write(full_html_content)


def create_html_plots(config, plots, title):
    if config.htmlColumns == 1:
        figur_links = '<div style="text-align: left; margin-top: 1px;">'
        figur_links += '<h4>Figures:</h4>'
        for p in plots:
            plot_title: str = p['layout']['title']['text']  # type: ignore
            figur_links += f'<a href="#{plot_title}">{plot_title}</a>&emsp;'

        figur_links += '</div>'
    else:
        figur_links = ''
    html_content = '<h1>' + title + '</h1>'
    html_content += figur_links
    for p in plots:
        plot_title: str = p['layout']['title']['text']  # type: ignore
        html_content += f'<div id="{plot_title}">' + p.to_html(full_html=False,
                                                               include_plotlyjs='cdn') + '</div>'  # type: ignore
    return html_content


def readCasesheet(casesheetPath : str) -> Dict[int, str]:
    '''
    Reads optional casesheets and provides dict mapping rank to case title.
    '''

    try:
        pd.read_excel(casesheetPath, sheet_name='RfG cases', header=1) # type: ignore
    except FileNotFoundError:
        print(f'Casesheet not found at {casesheetPath}.')
        return dict()
    
    cases : List[Case] = list()
    for sheet in ['RfG', 'DCC', 'Unit', 'Custom']:
        dfc = pd.read_excel(casesheetPath, sheet_name=f'{sheet} cases', header=1) # type: ignore
        for _, case in dfc.iterrows(): # type: ignore
            cases.append(Case(case)) # type: ignore

    caseDict : Dict[int, str] = defaultdict(lambda: 'Unknown case')
    for case in cases:
        caseDict[case.rank] = case.Name
    return caseDict

def main() -> None:
    config = ReadConfig()
    
    print('Starting plotter main thread')

    #Output config
    print('Configuration:')
    for setting in config.__dict__:
        print(f'\t{setting}: {config.__dict__[setting]}')

    print()

    resultDict = mapResultFiles(config)
    figureDict = readFigureSetup('figureSetup.csv')
    rankDict = readRankSetup('rankSetup.csv')
    caseDict = readCasesheet(config.optionalCasesheet)
    colorSchemeMap = colorMap(resultDict)

    if not exists(config.resultsDir):
        makedirs(config.resultsDir)

    threads : List[Thread] = list()

    for rank in resultDict.keys():
        if config.threads > 1:
            threads.append(Thread(target = drawPlot, args = (rank, resultDict, figureDict, caseDict, colorSchemeMap, rankDict, config)))
        else:
            drawPlot(rank, resultDict, figureDict, caseDict, colorSchemeMap, rankDict, config)
    
    NoT = len(threads)
    if NoT > 0:  
        sched = threads.copy()
        inProg : List[Thread] = []

        while len(sched) > 0:
            for t in inProg:
                if not t.is_alive():
                    print(f'Thread {t.native_id} finished')
                    inProg.remove(t)

            while len(inProg) < config.threads and len(sched) > 0:
                nextThread = sched.pop()
                nextThread.start()
                print(f'Started thread {nextThread.native_id}')
                inProg.append(nextThread)

            time.sleep(0.5)

    print('Finished plotter main thread')

if __name__ == "__main__":
    main()

if LOG_FILE:
    LOG_FILE.close()