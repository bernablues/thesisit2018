# thesisit2018
SDVDTN

## MySQL Database Schema
### Bundles
*id int(11)
*type int(11)
*seq int(11)
*sid int(11)
*payload varchar(10000)
### sensor_data
*id int(11)
*timestamp datetime
*seq_number int(11)
*data varchar(1000)
### routing_table
*bundle_id int(11)
*sensor_id int(11)
*sent_to varchar(15)


