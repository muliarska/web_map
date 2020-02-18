# web_map
The user enters the year and coordinates of the location for which he wants to build the map (in format (latitude, longitude)). The map is generated and the user receives the HTML file as a result. Up to 10 labels are placed on the map, each corresponding to the closest locations to that specified by the user. The map only shows locations where movies were made in the year the user specified. By clicking on the tag you can see a movie or several movies that were shot at this location this year. These labels are the second layer of the map. The third layer contains 5 round colored labels that correspond to the top 5 countries where the highest quality films were shot. This is the information from survey in 2018.

### Prerequisites:
Modules folium and geopy must be installed.

### HTML file structure:
File is stored in three sections: head, body i script. The <! DOCTYPE> element is intended to indicate the type of the current document - DTD (document type definition, description of the type of document). The <html> tag defines the beginning of the HTML file, the header (<head>) and the document body (<body>) are stored inside it. With the <meta> tag you can change the page encoding, add keywords, document description and much more. The <style> tag is used to define styles for web page elements. Be sure to add the closing </head> tag to indicate that the title block of the document is complete. The body of the <body> document is intended for placement of tags and content of the web page. The <script> tag is designed to be connected with a standard document.

### An example of running the program:
`Please enter a year you would like to have a map for: 
2001`
`Please enter your location (format: lat, long): 
52.5170365, 13.3888599`
`Map is generating...`
`Please wait...`
`Finished. Please have look at the map movies_map.html`

![(example1.PNG)]

![(example2.PNG)]

### Conclusion:
The map shows the tags of the nearby locations where the films were made and what the movies are. The other layer also shows 5 countries where film production is the highest quality.

## Author: Yana Muliarska
