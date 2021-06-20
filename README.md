# Social-Distancing Using Edge Computing

This project aims to develop a solution to solve the need for a smart technology to help chain business owners to maintain stronger social distancing measures to be followed by their customers and employees in their respective business (mainly focusing on restaurants) and, therefore, help them avoid hefty fines from the government and also help reduce the risk of spreading the COVID-19 virus.

The solution is an AI object detecting algorithm we are developing that will be able to detect people in a restaurant and identify social distancing violations conducted by employees and customers in restaurants by calculating if the distance between two people is less than 1.5 meters and inform the manager or the owner of the respective restaurants about the violations in the form of notifications in a custom-built mobile and web application. 

The custom-made mobile application will be developed using Flutter, an open-source UI software development kit created by Google which will be linked to a database storing platform called Firebase. The application will be available in two platforms, Android & iPhone. Similarly, a web application was also created using React.js.

The object detection algorithm will be derived from The YOLO v4 object detection algorithm. The  algorithm was run on NVIDIA Jetson Nano Developer Kit and the Raspberry Pi 4 for inferencing.

# Limitations
The camera used in the smart system to monitor people must be in a stationary position and fixed in such a way that the angle is top-down. If the camera is fixed on the ground or on a tripod, the accuracy of the results will be reduced. 
