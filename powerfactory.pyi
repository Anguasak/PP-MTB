#type: ignore
from typing import Any, Optional, overload
from typing import List, Union # Added by Energinet
from enum import Enum

class DataObject:
    class AttributeType(Enum):
        INVALID = -1
        INTEGER = 0
        INTEGER_VEC = 1
        DOUBLE = 2
        DOUBLE_VEC = 3
        DOUBLE_MAT = 4
        OBJECT = 5
        OBJECT_VEC = 6
        STRING = 7
        STRING_VEC = 8
        INTEGER64 = 9
        INTEGER64_VEC = 10

    @overload
    def AddCopy(self, __objectToCopy: 'DataObject', *__partOfName: int|str) -> 'DataObject': ...
    @overload
    def AddCopy(self, __objectsToCopy: list) -> 'DataObject': ...

    def CopyData(self, __source: 'DataObject') -> None: ...

    def CreateObject(self, __className: str, *__objectNamePart: int|str) -> 'DataObject': ...

    def Delete(self) -> int: ...

    def Energize(self, __resetRA: Optional[int]) -> list: ...

    def GetAttribute(self, __name: str) -> Any: ...

    def GetAttributeDescription(self, __name: str, __short: int = 0) -> str: ...

    def GetAttributeLength(self, __name: str) -> int: ...

    def GetAttributeShape(self, __name: str) -> list: ...

    def GetAttributeType(self, __name: str) -> AttributeType: ...

    def GetAttributeUnit(self, __name: str) -> str: ...

    def GetAttributes(self) -> list: ...

    def GetChildren(self, __hiddenMode: int, __filter: Optional[str], __subfolders: Optional[int]) -> list: ...

    def GetClassName(self) -> str: ...

    def GetCombinedProjectSource(self) -> 'DataObject': ...

    def GetConnectedElements(self, __rBrk: Optional[int], __rDis: Optional[int], __rOut: Optional[int]) -> list: ...

    def GetConnectionCount(self, __includeNeutral: int = 0) -> int: ...

    def GetContents(self, __Name: Optional[str], __recursive: Optional[int]) -> List[DataObject]: ... #Edited by Energinet

    def GetControlledNode(self, __bus: int, __check: Optional[int]) -> list: ...

    def GetCubicle(self, __side: int) -> 'DataObject': ...

    def GetFullName(self, __type: Optional[int] = None) -> str: ...

    def GetImpedance(self, __refVoltage: float, __i3Trf: Optional[int]) -> list: ...

    def GetInom(self, __busIndex: int = 0, __inclChar: int = 0) -> float: ...

    def GetNode(self, __busIndex: int, __considerSwitches: int = 0) -> 'DataObject': ...

    def GetOperator(self) -> 'DataObject': ...

    def GetOwner(self) -> 'DataObject': ...

    def GetParent(self) -> 'DataObject': ...

    def GetReferences(self, __filter: str = '*', __includeSubsets: int = 0, __includeHiddenObjects: int = 0) -> list: ...

    def GetRegion(self) -> int: ...

    def GetSupplyingSubstations(self) -> list: ...

    def GetSupplyingTransformers(self) -> list: ...

    def GetSupplyingTrfstations(self) -> list: ...

    def GetSystemGrounding(self) -> int: ...

    def GetUnom(self, __busIndex: int = 0) -> float: ...

    def GetUserAttribute(self, __attName: str) -> list: ...

    def GetZeroImpedance(self, __refVoltage: float, __i3Trf: Optional[int]) -> list: ...

    def HasAttribute(self, __name: str) -> int: ...

    def HasReferences(self) -> int: ...

    def HasResults(self, __ibus: Optional[int]) -> int: ...

    def IsCalcRelevant(self) -> int: ...

    def IsDeleted(self) -> int: ...

    def IsEarthed(self) -> int: ...

    def IsEnergized(self) -> int: ...

    def IsHidden(self) -> int: ...

    def IsInFeeder(self, __Feeder: 'DataObject', __OptNested: int = 0) -> int: ...

    def IsNetworkDataFolder(self) -> int: ...

    def IsNode(self) -> int: ...

    def IsObjectActive(self, __time: int) -> int: ...

    def IsObjectModifiedByVariation(self, __considerADD: int, __considerDEL: int, __considerDELTA: int) -> int: ...

    def IsOutOfService(self) -> int: ...

    def IsReducible(self) -> int: ...

    def IsShortCircuited(self) -> int: ...

    def Isolate(self, __resetRA: Optional[int], __isolateCBs: Optional[int]) -> list: ...

    def MarkInGraphics(self, __searchAllDiagramsAndSelect: int = 0) -> None: ...

    @overload
    def Move(self, __objectToMove: 'DataObject') -> int: ...
    @overload
    def Move(self, __objectsToMove: list) -> int: ...

    @overload
    def PasteCopy(self, __objectToCopy: 'DataObject', __resetMissingReferences: int = 0) -> list: ...
    @overload
    def PasteCopy(self, __objectsToCopy: list) -> int: ...

    def PurgeUnusedObjects(self) -> None: ...

    def ReportUnusedObjects(self) -> None: ...

    def SearchObject(self, __name: str) -> Optional['DataObject']: ... #Optional[Union['DataObject', 'ComPython', 'ElmRes', 'IntPrj']]: ... #Edited by Energinet

    def SetAttribute(self, __name: str, __value: Any) -> None: ...

    def SetAttributeLength(self, __name: str, __length: int) -> int: ...

    def SetAttributeShape(self, __name: str, __shape: list) -> int: ...

    def SetAttributes(self, __values: list) -> None: ...

    def ShowEditDialog(self) -> int: ...

    def ShowModalSelectTree(self, __title: Optional[str], __filter: Optional[str]) -> 'DataObject': ...

    def SwitchOff(self, __resetRA: Optional[int], __simulateOnly: Optional[int]) -> list: ...

    def SwitchOn(self, __resetRA: Optional[int], __simulateOnly: Optional[int]) -> list: ...

    def WriteChangesToDb(self) -> None: ...


class OutputWindow:
    class MessageType(Enum):
        Plain = 0
        Error = 1
        Warn = 2
        Info = 4

    def Clear(self) -> None: ...

    def Flush(self) -> None: ...

    @overload
    def GetContent(self) -> list: ...
    @overload
    def GetContent(self, __filter: MessageType) -> list: ...

    @overload
    def Print(self, __message: str) -> None: ...
    @overload
    def Print(self, __type: MessageType, __message: str) -> None: ...

    def Save(self, __filePath: str) -> None: ...

    def SetState(self, __newState: int) -> None: ...


class Application:
    def ActivateProject(self, __name: str) -> int: ...

    def ActivateVariations(self, __variations: list) -> None: ...

    def ClearOutputWindow(self) -> None: ...

    def ClearRecycleBin(self) -> None: ...

    def CloseTableReports(self) -> None: ...

    def CommitTransaction(self) -> None: ...

    def ConvertGeometryStringToMDL(self, __orgString: str, __intGrfOrLayer: DataObject) -> str: ...

    def CreateFaultCase(self, __elms: set, __mode: int, __createEvt: int = 0, __folder: DataObject = None) -> int: ...

    @overload
    def CreateProject(self, __projectName: str, __gridName: str, __parent: DataObject = None) -> DataObject: ...
    @overload
    def CreateProject(self, __projectName: str, __parent: DataObject = None) -> DataObject: ...

    def DeactivateVariations(self, __variations: list) -> None: ...

    def DecodeColour(self, __encodedColour: int) -> list: ...

    def DefineTransferAttributes(self, __classname: str, __attributes: str) -> None: ...

    @overload
    def DeleteUntouchedObjects(self, __grid: DataObject) -> int: ...
    @overload
    def DeleteUntouchedObjects(self, __grids: list) -> int: ...

    def EchoOff(self) -> None: ...

    def EchoOn(self) -> None: ...

    def EncodeColour(self, __red: int, __green: int, __blue: int, __alpha: int = 255) -> int: ...

    def ExecuteCmd(self, __command: str) -> None: ...

    def FlushOutputWindow(self) -> None: ...

    def GetActiveCalculationStr(self) -> str: ...

    def GetActiveNetworkVariations(self) -> list: ...

    def GetActiveProject(self) -> Optional[DataObject]: ... #Edited by Energinet

    def GetActiveScenario(self) -> DataObject: ...

    def GetActiveScenarioScheduler(self) -> DataObject: ...

    def GetActiveStages(self, __variedFolder: DataObject = None) -> list: ...

    def GetActiveStudyCase(self) -> Optional[DataObject]: ... #Optional added by Energinet

    def GetAttributeDescription(self, __classname: str, __name: str, __short: int = 0) -> str: ...

    def GetAttributeUnit(self, __classname: str, __name: str) -> str: ...

    def GetBorderCubicles(self, __element: DataObject) -> list: ...

    def GetBrowserSelection(self) -> list: ...

    def GetCalcRelevantObjects(self, __nameFilter: str = "*.*", __includeOutOfService: int = 1, __topoElementsOnly: int = 0, __bAcSchemes: int = 0) -> list: ...

    def GetClassDescription(self, __name: str) -> str: ...

    def GetClassId(self, __className: str) -> int: ...

    def GetCurrentDiagram(self) -> DataObject: ...

    def GetCurrentScript(self) -> DataObject: ...

    def GetCurrentSelection(self) -> list: ...

    def GetCurrentUser(self) -> DataObject: ...

    def GetCurrentZoomScale(self) -> int: ...

    def GetDataFolder(self, __classname: str, __iCreate: int = 0) -> DataObject: ...

    def GetDesktop(self) -> DataObject: ...

    def GetDiagramSelection(self) -> list: ...

    def GetFlowOrientation(self) -> int: ...

    def GetFromStudyCase(self, __className: str) -> Optional['DataObject'] : ... #Optional[Union[DataObject,'ElmRes', 'SetDesktop']] : ...

    def GetGlobalLibrary(self, __ClassName: str = "") -> DataObject: ...

    def GetInstallationDirectory(self) -> str: ...

    def GetInterfaceVersion(self) -> int: ...

    def GetLanguage(self) -> str: ...

    def GetLocalLibrary(self, __ClassName: str = "") -> DataObject: ...

    def GetMem(self, __calculateDelta: int = 0, __inMegaByte: int = 0) -> int: ...

    def GetOutputWindow(self) -> OutputWindow: ...

    def GetProjectFolder(self, __type: str, __create: int = 0) -> Optional[DataObject]: ... #Optional added by Energinet

    def GetRandomNumber(self, __x1: Optional[float], __x2: Optional[float]) -> float: ...

    def GetRandomNumberEx(self, __distribution: int, __p1: Optional[float], __p2: Optional[float]) -> float: ...

    def GetRecordingStage(self) -> DataObject: ...

    def GetSettings(self, __key: str) -> str: ...

    def GetSummaryGrid(self) -> DataObject: ...

    def GetTableReports(self) -> list: ...

    def GetTemporaryDirectory(self) -> str: ...

    @overload
    def GetTouchedObjects(self, __varOrStage: object) -> list: ...
    @overload
    def GetTouchedObjects(self, __varsAndStages: list) -> list: ...

    @overload
    def GetTouchingExpansionStages(self, __rootObject: object) -> list: ...
    @overload
    def GetTouchingExpansionStages(self, __rootObjects: list) -> list: ...

    @overload
    def GetTouchingStageObjects(self, __rootObject: object) -> list: ...
    @overload
    def GetTouchingStageObjects(self, __rootObjects: list) -> list: ...

    @overload
    def GetTouchingVariations(self, __rootObject: object) -> list: ...
    @overload
    def GetTouchingVariations(self, __rootObjects: list) -> list: ...

    def GetUserManager(self) -> DataObject: ...

    def GetUserSettings(self, __user: object = None) -> object: ...

    def GetWorkspaceDirectory(self) -> str: ...

    def Hide(self) -> None: ...

    def ImportDz(self, __target: DataObject, __dzFilePath: str) -> list: ...

    def ImportSnapshot(self, __dzsFilePath: str) -> list: ...

    def InvertMatrix(self, __realPart: DataObject, __imaginaryPart: Optional[DataObject]) -> int: ...

    def IsAttributeModeInternal(self) -> int: ...

    def IsAutomaticCalculationResetEnabled(self) -> int: ...

    def IsFinalEchoOnEnabled(self) -> int: ...

    def IsLdfValid(self) -> int: ...

    def IsNAN(self, __value: float) -> int: ...

    def IsRmsValid(self) -> int: ...

    def IsScenarioAttribute(self, __classname: str, __attributename: str) -> int: ...

    def IsShcValid(self) -> int: ...

    def IsSimValid(self) -> int: ...

    def IsWriteCacheEnabled(self) -> int: ...

    def LicenceHasModule(self, __module: str) -> int: ...

    def LoadProfile(self, __profileName: str) -> int: ...

    def MarkInGraphics(self, __objects: list, __searchOpenedDiagramsOnly: int = 0) -> None: ...

    def OutputFlexibleData(self, __objects: list, __flexibleDataPage: str = '') -> None: ...

    @overload
    def PostCommand(self, __commandString: str) -> None: ...
    @overload
    def PostCommand(self, __command: DataObject) -> None: ...

    @overload
    def PrepForUntouchedDelete(self, __grid: DataObject) -> None: ...
    @overload
    def PrepForUntouchedDelete(self, __grids: list) -> None: ...

    def PrintError(self, __message: str) -> None: ...

    def PrintInfo(self, __message: str) -> None: ...

    def PrintPlain(self, __message: str) -> None: ...

    def PrintWarn(self, __message: str) -> None: ...

    def Rebuild(self, __iMode: int = 1) -> None: ...

    def ReleaseData_(self) -> None: ...

    def ReleaseMemory_(self) -> None: ...

    def ReloadProfile(self) -> None: ...

    def ResGetData(self, __resultObject: DataObject, __iX: int, __col: Optional[int]) -> list: ...

    def ResGetDescription(self, __resultObject: DataObject, __col: int, __ishort: Optional[int]) -> str: ...

    @overload
    def ResGetFirstValidObject(self, __resultFile: DataObject, __row: int, __classNames: Optional[str], __variableName: Optional[str], __limit: Optional[float], __limitOperator: Optional[int], __limit2: Optional[float], __limitOperator2: Optional[int]) -> int: ...
    @overload
    def ResGetFirstValidObject(self, __resultFile: Optional[DataObject], __row: Optional[int], __objects: Optional[list]) -> int: ...

    def ResGetFirstValidObjectVariable(self, __resultFile: DataObject, __variableNames: Optional[str]) -> int: ...

    def ResGetFirstValidVariable(self, __resultFile: DataObject, __row: int, __variableNames: Optional[str]) -> int: ...

    @overload
    def ResGetIndex(self, __resultFile: DataObject, __obj: DataObject, __varName: Optional[str]) -> int: ...
    @overload
    def ResGetIndex(self, __resultFile: DataObject, __obj: DataObject, __colIndex: Optional[int]) -> int: ...
    @overload
    def ResGetIndex(self, __resultFile: DataObject, __varName: Optional[str], __colIndex: Optional[int]) -> int: ...

    def ResGetMax(self, __resultFile: DataObject, __col: int) -> list: ...

    def ResGetMin(self, __resultFile: DataObject, __col: int) -> list: ...

    @overload
    def ResGetNextValidObject(self, __resultFile: DataObject, __classNames: Optional[str], __variableName: Optional[str], __limit: Optional[float], __limitOperator: Optional[int], __limit2: Optional[float], __limitOperator2: Optional[int]) -> int: ...
    @overload
    def ResGetNextValidObject(self, __resultFile: DataObject, __objects: list) -> int: ...

    def ResGetNextValidObjectVariable(self, __resultFile: DataObject, __variableNames: Optional[str]) -> int: ...

    def ResGetNextValidVariable(self, __resultFile: DataObject, __variableNames: Optional[str]) -> int: ...

    def ResGetObj(self, __resultObject: DataObject, __col: int) -> DataObject: ...

    def ResGetUnit(self, __resultObject: DataObject, __col: int) -> str: ...

    def ResGetValueCount(self, __resultObject: DataObject, __col: Optional[int]) -> int: ...

    def ResGetVariable(self, __resultObject: DataObject, __col: int) -> str: ...

    def ResGetVariableCount(self, __resultObject: DataObject) -> int: ...

    def ResLoadData(self, __resultObject: DataObject) -> None: ...

    def ResReleaseData(self, __resultObject: DataObject) -> None: ...

    def ResSortToVariable(self, __resultObject: DataObject, __col: int) -> int: ...

    def ResetCalculation(self) -> None: ...

    def RndExp(self, __rate: float, __rngNum: Optional[int]) -> float: ...

    def RndGetMethod(self, __rngNum: Optional[int]) -> str: ...

    def RndGetSeed(self, __rngNum: Optional[int]) -> int: ...

    def RndNormal(self, __mean: float, __stddev: float, __rngNum: Optional[int]) -> float: ...

    def RndSetup(self, __seedAutomatic: int, __seed: Optional[int], __rngType: Optional[int], __rngNum: Optional[int]) -> None: ...

    def RndUnifInt(self, __min: int, __max: int, __rngNum: Optional[int]) -> int: ...

    def RndUnifReal(self, __min: float, __max: float, __rngNum: Optional[int]) -> float: ...

    def RndWeibull(self, __shape: float, __scale: float, __rngNum: Optional[int]) -> float: ...

    def SaveAsScenario(self, __pName: str, __iSetActive: int) -> DataObject: ...

    def SearchObjectByForeignKey(self, __foreignKey: str) -> DataObject: ...

    def SearchObjectsByCimId(self, __cimId: str) -> list: ...

    def SelectToolbox(self, __toolbar: int, __groupName: str, __toolboxName: str) -> int: ...

    def SetAttributeModeInternal(self, __internalMode: int) -> None: ...

    def SetAutomaticCalculationResetEnabled(self, __enabled: int) -> None: ...

    def SetFinalEchoOnEnabled(self, __enabled: int) -> None: ...

    def SetGraphicUpdate(self, __enabled: int) -> None: ...

    def SetGuiUpdateEnabled(self, __enabled: int) -> int: ...

    def SetInterfaceVersion(self, __version: int) -> int: ...

    def SetOutputWindowState(self, __newState: int) -> None: ...

    def SetProgressBarUpdatesEnabled(self, __enabled: int) -> int: ...

    def SetRandomSeed(self, __seed: int) -> None: ...

    def SetShowAllUsers(self, __enabled: int) -> int: ...

    def SetUserBreakEnabled(self, __enabled: int) -> None: ...

    def SetWriteCacheEnabled(self, __enabled: int) -> None: ...

    def Show(self) -> None: ...

    def ShowModalBrowser(self, __objects: list, __detailMode: int = 0, __title: str = '', __page: str = '') -> None: ...

    def ShowModalSelectBrowser(self, __objects: list, __title: Optional[str], __classFilter: Optional[str], __page: str = '') -> list: ...

    def ShowModelessBrowser(self, __objects: list, __detailMode: int = 0, __title: str = '', __page: str = '') -> None: ...

    def SplitLine(self, __Line: DataObject, __percent: float = 50, __createSwitchSide0: int = 0, __createSwitchSide1: int = 0, __graphicSplit: int = 0) -> DataObject: ...

    def StatFileGetXrange(self) -> list: ...

    def StatFileResetXrange(self) -> None: ...

    def StatFileSetXrange(self, __min: float, __max: float) -> None: ...

    def UpdateTableReports(self) -> None: ...

    def WriteChangesToDb(self) -> None: ...


def GetApplication(__username: str = None, __password: str = None, __commandLineArguments: str = None) -> Optional[Application]: ... #Optional added by Energinet

def GetApplicationExt(__username: str = None, __password: str = None, __commandLineArguments: str = None) -> Optional[Application]: ... #Optional added by Energinet

# Added by Energinet
class ComPython(DataObject):
    
    def GetExternalObject(self, __name: str) -> List[Union[int, Optional[DataObject]]]: ...

    def GetInputParameterDouble(self, __name: str) -> List[Union[int, float]]: ...

    def GetInputParameterInt(self, __name: str) -> List[Union[int, int]]: ...

    def GetInputParameterString(self, __name: str) -> List[Union[int, str]]: ...

class ComDpl(DataObject):

    def Execute(self) -> int: ...

class ComTasks(DataObject):

    def AppendCommand(self, __command: DataObject, __row : Optional[int] = -1) -> int: ...

    def AppendStudyCase(self, __studyCase: DataObject) -> int: ...

    def Execute(self) -> None: ...

class ComRes(DataObject):
    
    def Execute(self) -> None: ...

class ElmRes(DataObject):

    def AddVariable(self, __element : DataObject, __varname: str, ) -> int: ...

class ElmNet(DataObject):

    def Activate(self) -> int: ...

class IntPrj(DataObject):

    def Activate(self) -> int: ...
    
    def Deactivate(self) -> int: ...

    def CreateVersion(self, __name: str) -> DataObject: ...

class IntCase(DataObject):
        
        def Activate(self) -> int: ...
        
        def Deactivate(self) -> int: ...

        def Consolidate(self) -> int: ...

        def SetStudyTime(self, __datetime : int) -> None: ...

class IntScheme(DataObject):
    def Activate(self) -> int: ...

class IntSstage(DataObject):
    def Activate(self) -> int: ...

class SetDesktop(DataObject):

    def GetPage(self, __name: str, __create: int = 0, cls : str = '') -> DataObject: ...

class GrpPage(DataObject):

    def RemovePage(self) -> None: ...

    def GetOrInsertPlot(self, __name : str, __type : int, __create : int = 1) -> DataObject: ...

class PltLinebarplot(DataObject):
    def GetDataSeries(self) -> DataObject : ...

    def DoAutoScale(self, __axis: Optional[int] = None) -> None: ...

class PltDataseries(DataObject)
    def AddCurve(self, __element : DataObject, __varname : str, __datasource : Optional[DataObject] = None) -> None: ...