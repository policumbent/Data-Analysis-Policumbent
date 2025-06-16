# Messaggi NMEA da gnss

- GPGGA --> __Global Positioning System Fix Data__  time, position and fix related data of the GNSS receiver
- GNS --> Global Navigation Satellite System (GNSS) fix data, encompassing information from multiple satellite constellations such as GPS, GLONASS, Galileo, BeiDou, and QZSS. This sentence is particularly useful for receivers utilizing multiple GNSS constellations to determine position
- GPGST --> Reflects the accuracy of the solution type used in the BESTPOS and GPGGA logs. It includes the root mean square (RMS) value of pseudorange residuals, error ellipse semi-major and semi-minor axes, error ellipse orientation, and 1-sigma errors for latitude, longitude, and height
- GPRMC --> This log contains time, date, position, track made good and speed data provided by the GPS navigation receiver
- GSA --> GPS receiver operating mode, satellites used in the navigation solution reported by the GGA or GNS sentence and DOP values
- GSV --> Number of satellites (SV) in view, satellite ID numbers, elevation, azimuth, and SNR value. Four satellites maximum per transmission.
- PSTMVER --> __Firmware Version__ Reports the firmware version of the GNSS receiver. This information is useful for verifying the software version and ensuring compatibility with other systems.
- PSTMAGPSSTATUS --> __GPS Status__ Provides the current status of the GPS receiver, including information on signal quality, fix status, and other operational parameters.
- PSTMGEOFENCE --> __Geofence Status__ Indicates the status of geofence boundaries, including whether the receiver is inside or outside predefined geographic areas.
- PSTMODO --> __OPRETIONAL MODE__ Reports the current operational mode of the GNSS receiver, such as autonomous, differential, or simulated mode
- PSTMDATALOG --> __Data Logging Status__ Provides information on the status of data logging, including whether logging is active and the amount of data stored.
- PSTMSGL --> __Message Logging__ Logs messages related to the receiver's operation, including errors, warnings, and status updates.
- PSTMSAVEPAR --> __Save Parameters__ Saves the current configuration parameters of the GNSS receiver, allowing for easy restoration of settings after power cycles or resets