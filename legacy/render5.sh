#!/bin/bash
# render5.sh DIR POLLFILE [chrome args...] URL
# Headless chrome here writes the output but never exits; poll for the file then kill by profile dir.
DIR="$1"; POLL="$2"; shift 2
CH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cd /Users/zhw/.qoderwork/workspace/mtmqoy4hwvnd8s3g || exit 1
rm -f "$POLL"
pkill -f "headless=new" 2>/dev/null; sleep 1
if echo "$*" | grep -q -- "--dump-dom"; then
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --user-data-dir="$DIR" "$@" >"$POLL" 2>/dev/null &
else
  "$CH" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --user-data-dir="$DIR" "$@" >/dev/null 2>&1 &
fi
for i in $(seq 1 140); do
  sleep 2
  if [ -s "$POLL" ]; then sleep 2; break; fi
done
pkill -f "user-data-dir=$DIR" 2>/dev/null
pkill -f "headless=new" 2>/dev/null
if [ -s "$POLL" ]; then echo "OK $POLL $(wc -c <"$POLL" | tr -d ' ') bytes"; else echo "FAIL $POLL"; exit 1; fi
