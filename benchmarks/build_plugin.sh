cd plugin
rm CMakeCache.txt
cmake -D ASPECT_DIR=../../aspect/build .
make
cd ..
