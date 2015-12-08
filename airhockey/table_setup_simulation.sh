#!/bin/bash

SOURCE=$1
FPS=$2

CAPTURE_CONF=source=$SOURCE
if [ "$FPS" != "" ]; then
	CAPTURE_CONF=$CAPTURE_CONF,fps=$FPS
fi

python airhockey/main.py \
	record.TableSetupCapture:$CAPTURE_CONF \
	puck_module.TableSetupPuckDetection \
	strategy.SimpleStrategy \
	visualize.TableSetupSimulationImageDisplay
