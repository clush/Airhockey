#!/bin/bash

SOURCE=$1
FPS=$2

CAPTURE_CONF=source=$SOURCE
if [ "$FPS" != "" ]; then
	CAPTURE_CONF=$CAPTURE_CONF,fps=$FPS
fi
	
#if [ "$3" == "-r" ]; then
#	python airhockey/main.py \
#	      record.TableSetupCapture:$CAPTURE_CONF \
#	      puck_module.TableSetupPuckDetection \
#	      visualize.TableSetupImageDisplay
#fi

python airhockey/main.py \
	record.TableSetupCapture:$CAPTURE_CONF \
	puck_module.TableSetupPuckDetection \
	visualize.TableSetupImageDisplay \
	Connection.Strategy
