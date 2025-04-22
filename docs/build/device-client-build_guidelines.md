# Onboard Device Client Build

- Set up a C++ Development environment on the linux machine.
- If not already installed, install the following software components.
```
* [cmake] sudo apt install cmake
* [zlib] sudo apt install zlib1g-dev
* [sqlite] sudo apt-get install libsqlite3-dev
* [curl] sudo apt-get install libcurl4-openssl-dev
* [ssl] sudo apt-get install libssl1.0-dev
* [crypto] sudo apt-get install libcrypto++-dev
* [zmq] sudo apt-get install libzmq3-dev
```

- After installing the software components, build the device client as follows:
```
<working-directory>\device-client\client> ls -l
\deviceclient
\libClientBL
\libCore
\libAuto
\libNetwork
\libDevice
\libUtils
\libEvent
\libmosquitto
\CMakeLists.txt
 
<working-directory>\device-client\client> mkdir build
<working-directory>\device-client\client> cd build
<working-directory>\device-client\client\build> cmake ..
<working-directory>\device-client\client\build> make
```
- After building the device client, the deviceclient binary file can be found in the ```.\bin\``` folder and the libEvent.so file can be found in the ```.\lib\``` folder.
- Load the `deviceclient` binary file into the target device, for example: /usr/bin.
- Load the `libEvent.so` shared library file into the target device, for example: /usr/lib.
- Also, load the configuration and cert files that are in the device-client/assets/ folder into the target device, for example: assets/config or /usr/config etc.

## Build the Device Client using GitHub Actions
- The device client is packaged as a standalone C++ distribution using cmake and the apt-get command line tool.
- To run the build, the workflow requires the following software components installed on the server.
```
* [cmake] sudo apt install cmake
* [zlib] sudo apt install zlib1g-dev
* [sqlite] sudo apt-get install libsqlite3-dev
* [curl] sudo apt-get install libcurl4-openssl-dev
* [ssl] sudo apt-get install libssl1.0-dev
* [crypto] sudo apt-get install libcrypto++-dev
* [zmq] sudo apt-get install libzmq3-dev
```
- The workflow is configured to run on GitHub-hosted `ubuntu` server and has some pre-installed components.
- The workflow loads the `deviceclient` binary file into the temporary directory location.
- The workflow loads the `libEvent.so` shared library file into the temporary directory location.
- The workflow loads the configuration and cert files into a read-only assets/config path.
- The workflow bundles all the files and the uploads the `deviceclient.zip` file to the artifacts location of the run action.
```yaml
steps:
    - uses: actions/checkout@v4
    - name: make
      run: |
        sudo apt-get install libcurl4-openssl-dev
        sudo apt-get install libzmq3-dev
        cd client
        mkdir build
        cd build
        cmake ..
        make

        # create temporary artifacts directory
        pwd
        mkdir afacts
        
        # copy the build artifacts to the afacts directory
        cp bin/deviceclient afacts/
        cp lib/libEvent.so afacts/
        cp lib/libDevice.so afacts/
        cp ../../assets/cacert.pem afacts/
        cp ../../assets/server-cert.pem afacts/
        cp ../../assets/eks-core-qa.conf afacts/

    # copy the build artifacts to artifacts location
    - uses: actions/upload-artifact@v4
      with:
        name: deviceclient
        path: /home/runner/work/device-client/device-client/client/build/afacts
```

