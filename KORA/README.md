# Documentation for v_max.py 
------

The goal of this simple script is to provide a visual representation of the varying impact that multiple parameters can have on the theoretical cruise speed of a vehicle.
The specific vehicle is KORA and is supposed to leverage both human and electric power. 

## Prerequisites

This is a Python3 script. It can be executed by any PC that has python 3 installed (winget or any packege manager, or from the official python website) and modified in any text editor or IDE such as Notepad or VSCode (try VSCodium for a telemetry free version!).
You will also need to have numpy and matplotlib installed. These are basic libraries and will be installed using pip, the preferred python package manager. Installation can be slightly different based on your OS but is WIDELY documented on the internet.  


## Basic Assumptions

By theorectical cruise speed we mean the speed at which KORA could theoretically sustain prolonged usage and would be battery energy limited rather battery power limited. In other terms everything is at steady state and the electrical power is set as the e-Motor nominal power rather than its peak. This ensures reliable sustained performance. 

The longitudinal dynamics model here implented is very basic and neglects apparent inertial masses and any type of inertial contribution, given this is meant to be a representation of steady state cruising. As for right now, rolling resistance is also assumed to be independent from speed and basically just guessed. 

No ground gradient is considered, although it could be easily implemented. 

It is also worth noting that we assume that a percentage increase in any of the tested parameters has the same resource requirements thoughout. This is probably wrong but it doesn't affect the results, just the way they should be read. 

By comparing the impact of standardized variations of relevant parameters in terms of the speed that they grant or take away, we hope to help prioritize certain aspects of the reasearch and development process both early and late stage. 

## The Code

First up is the initialization of the base values for the parameters of interest. These values will be used as the center of our analysis. All the tested variations will be AROUND these values. 
For example, if the electric nominal power is set to 250W, then the script will test the theoretical cruising speed for values ranging from (250x0.5) to (250x1.5), meaning within a +-50% interval. 
This interval can be modified in the following section, where the max and min values for each of the tested parameters are defined. Symmetrical intervals are probably a good idea. 

An equally spaced array of 100 values within the specified limits and centered around the base value is then generated. The number of array elements must be kept consistent between x and y axis (just leave at 100 and get the percentage).

the xaxis array simply stores a linspace of 100 elements within the requested +-50% interval so that the speed array from multiple tests can be plotted against a stable quantity, which is the aim of the whole script. 

All the arrays containg the speed values at varying power, rolling resistance, coefficient of drag area and frontal area are then plotted and superimposed to one another so they can be compared. 

## A few considerations

Rolling resistance is the least impactful parameters and probalby tells us that going for more grip at the cost of more resistance might be a good tradeoff if it doesn't make turning the steering wheel to unwieldy.

Speed is the only parameter that seems to hit an horizontal asymptotic line. There is less and less to be gained from increasing the power over a certain limit; the higher you go, the less you gain. This is due to the cubic relationship of the speed to the aerodynamic drag wihich after a certain point just becomes too big to be overcome with just brute power. 

Talking about aero drag it is interesting (although predictable) to notice that CdA and Frontal Area have the same exact effect on the cruise speed. This means that lowering the CdA by 1% at the cost of an increase in frontal area of 1% effectively yields no gains in terms of the cruise speed. 