# PP-MTB
Connecting new electricity generation & demand facilities to the public transmission and distribution systems in Denmark requires grid compliance studies with both RMS/PDT and EMT models. The danish TSO Energinet conducts systemlevel RMS/PDT studies in [DIgSILENT Powerfactory](https://www.digsilent.de/en/powerfactory.html). EMT studies are done in [PSCAD](https://www.pscad.com/).

  Energinets PP-MTB (**P**ower**P**lant and **M**odel **T**est **B**ench) is a test bench for automation of studycase setup and simulation in both PowerFactory and PSCAD with external visualizing of results. The PP-MTB is meant as a tool to help guide in checking simulation and plant performance of RMS/PDT- and EMT-models in regards to the danish grid code and the requirements for simulation models. A set of predefined cases are available with the option to add custom cases or remove exisiting ones.
  The PP-MTB, originally an internal Energinet tool, has been open-sourced as an strategic initiative to support the grid connecting parties. 

  Latest release notes can be found under [Releases](https://github.com/Energinet-AIG/PP-MTB/releases).
  
  Read more about the regulations for grid connection of new facilities here: [danish](https://energinet.dk/regler/el/nettilslutning) or [english](https://en.energinet.dk/electricity/rules-and-regulations/regulations-for-new-facilities).

## Dependencies
  Dependencies are installed by running `pip install -r requirements.txt`  in the respective tool subfolder. Note that the PSCAD doesn't yet contain a "requirements.txt" file but rather a "01 Read me.txt" mentioning the required packages that you manually need.

## Getting Started
  To get started, follow the Quickstart Guides on the PP-MTB wiki [Home](https://github.com/Energinet-IG/PP-MTB/wiki) page of the [PP-MTB GitHub](https://github.com/Energinet-AIG/PP-MTB). Here you will find guides for the Excel-Sheet, PowerFactory, PSCAD and the plotter.

## Contribution
  If you are interested in contributing, please feel free to file an issue. This is done by using the PP-MTB [Issues](https://github.com/Energinet-AIG/PP-MTB/issues) tab. Here you can report bugs, feature requests or improvements, but please check for known issues beforehand. 

  When you file an issue, please try making it as specific and independent of other issues as possible. Make use of the Labels to hightlight what problem or tool the issue revolves arround. We encourage you to contribute with any bug, improvement or idea you might come across to help make this tool as useful and user-friendly as possible.

## Help
  For further questions or help, please check if the rest of the [README](https://github.com/Energinet-AIG/PP-MTB/blob/main/README.md) or the [Quickstart Guides](https://github.com/Energinet-AIG/PP-MTB/wiki) contains the answer, otherwise please contact either:

  * Mathias Bernhardt Bødker Kristensen at mkt@energinet.dk 
  * Casper Vestergård Lindgaard at cvl@energinet.dk 
