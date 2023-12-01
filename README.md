# SOMEF3SMP
This repository transforms the JSON file outputto a JSONLD compatible with the maSMP (Machine Actionable Software MAnagement Plan) schema. 

The application has two main configuration files:
* maSMP.jsonld with the schema in JSON-LD of the SMP
* mappings.json with the mappings needed to include information in the SMP JSON-LD file.

## Requirements

* Python 3.10

The application has been tested in Linux systems altought it doesn't need any special library so it could be compatible with other operative systems 

## How to install SOMEF2SMP

To install the application, you have to clone the repository.

```bash
git clone https://github.com/oeg-upm/somef2smp.git
```

You don't need to create a virtual environment because we use the standard libraries from Python.

## How to use SOMEF2SMP

The first step is to use SOMEF to download the JSON files from the repositories of an specific institution. As a test, you can find the JSON files of the MPDL (Max Plank Institute Digital Library) github repository in the folder somef_outputs.

In case you can test it with repositories from another institution, please, follow the instructions for the installation of the framework [SOCA](https://github.com/oeg-upm/soca). You will have to execute the two first steps: describe and extract. 

After you have the somef output files, you can run the application


```bash
python somef2smp.py outputs/
```

The application will generate all JSON-LD files based on the schema defined in the maSMP.jsonld file.

If you want to change the used mapping, you will have to change the content of the mappins.json file.

This is an example of the file.

```json
{
    "maSMP:versionControlSystem":{
        "type": "direct",
        "attribute_name":"url",
        "attribute_value":"https://github.com"
    },
    "schema:programmingLanguage":{
        "type": "somef",
        "attribute_name":"text",
        "attribute_value":"programming_languages"
},
```
The file is a dictionary where the keys are the identifiers used in the schema (see file maSMP) you want to use.

The attribute type show the method used to complete the SMP. There are two available: direct and somef.
* With direct, we add the value directly without processing. You can find the value in **attribute_value**, and the name of the attribute in **attribute_name**.
* With somef, the information will be added with the output of SOMEF. The **attribute_name** defines the name of the attribute and **attribute_value** the name of the field that contains the value provided by SOMEF.

Modifying this file, you will be able to generate any SMP (based on JSON-LD) using the results of SOMEF.

##Acknowledgements

The ACTIVITY was carried out during the maSMP hackathon at [ZB MED](https://www.zbmed.de/en/) sponsored by [NFDI4DataScience](https://www.nfdi4datascience.de/). NFDI4DataScience is a consortium funded by the German Research Foundation (DFG), project number 460234259.


