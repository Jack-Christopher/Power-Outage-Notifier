# Power Outage Notifier

**Description**:  
When a power outage occurs, the power is cut off. This is a problem for people who are using electronic devices, that's why people often need to know when a power outage is about to happen.
This tool 

Other things to include:

  - **Technology stack**: It was made in Python, using the next libraries:
    
    - regex 2022.3.15
    - colorama 0.4.4
    - selenium 4.0.0
    - beautifulsoup4 4.10.0

  - **Coverage**: It's a program that works just for Power Outages in Arequipa, Peru.

## Installation
Before you can use this tool, you need to install the following libraries: 
```
pip install -r requirements.txt
```

You can run it by double clicking the file, but thus it will just work once. In order to run it every time you start your computer, you should do the following:
- Download the project to your computer
- Create a shortcut to the file `main.py`
- Press Windows+R, then type `shell:startup`, then click OK or press enter

A File Explorer window will appear, that's the "Startup Folder", that's where the program files that run at startup are.

- Copy the shortcut file to the Startup Folder
- Restart your computer

The program will run every time you start your computer. Actually, the first time during the day.

## Usage

- When you run the program for the first time, a list of all the districts will be shown. Then you have to enter the number of the district you want to monitor.


- The first time you turn on your computer during the day, the program will check all the programmed Power Outages in the district you selected.

- The other times you turn on your computer, the program just will exit.

## License
Power Outage Notifier is released under the [MIT license](https://opensource.org/licenses/MIT).