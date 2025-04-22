# Mobile Application (App) Build

## Build the iOS Mobile SDK and App on Local
- Install `Xcode 15.4 and above` to run the VehicleConnectSDK on the local machine.
- Checkout the project, open `VehicleConnectSDK.xcworkspace` file from the project and run the build on the xcode.
- Post the successful build, find the `VehicleConnectSDK.framework` file in the product folder and add into your project.
- Use the following to import the SDK.
```
Import VehicleConnectSDK
```
- Use the `AppManager` instance, which is a class inside VehicleConnectSDK, to initialize the SDK.
- You can also download the [iOSVehicleConnectApp](https://github.com/eclipse-ecsp/iOSVehicleConnectApp) for reference to see how to call API methods.

### Build the App
- `iOSVehicleConnectApp` is written in Swift. It is compatible with iOS 16 and later and with iOS devices.
- Download the app source code and open the app using VehicleConnect.xcworkspace file.
- Run the build on the Xcode.


## Build the Android Mobile SDK and App on Local
- Install `Android Studio` to run VehicleConnectSDK on the local machine.
- Check out the project and open it using `Android Studio`.
- Run the ```gradle sync``` and do a rebuild.
- After a successful build, find the `androidVehicleConnectSDK-debug.aar` in thr `build/outputs/aar` folder and add it to your application project lib folder.
- Implement the SDK/aar file, which is added into the lib folder of your application project, by using implementation statement inside `build.gradle.kts` (app level)
```
implementation(files("libs/androidVehicleConnectSDK.aar"))
```
- Use the AppManager instance, which is a class inside the VehicleConnectSDK, to initialize the SDK.
- You can also download the [androidVehicleConnectApp](https://github.com/eclipse-ecsp/androidVehicleConnectApp) for reference to see how to call API methods.

### Build the App
- `androidVehicleConnectApp` is written in Kotlin. It is compatible with Android 7.0 (API level 24) and later and with Android devices.
- Download the app source code and open the application using Android Studio.
- Run ```gradle build``` to build the project



## Build the iOS Mobile SDK and App using GitHub Actions
- The SDK is written in Swift. It is compatible with iOS 16 and later and with iOS devices.
- The workflow is configured to run on `macos server` and uses an `ios simulator platform` to build the project.
- The `xcodebuild` tool is configured to generate the build artifacts.
- After a successful build, the `VehicleConnectSDK.framework` is uploaded to the artifacts location of run action.
```xml
    steps:
        - name: Checkout
        uses: actions/checkout@v4
        - name: Set Default Scheme
        run: |
        cd VehicleConnectSDK
        scheme_list=$(xcodebuild -list -json | tr -d "\n")
        default=$(echo $scheme_list | ruby -e "require 'json'; puts JSON.parse(STDIN.gets)['project']['targets'][0]")
        echo $default | cat >default
        echo Using default scheme: $default
        - name: Build
        env:
        scheme: ${{ 'default' }}
        platform: ${{ 'iOS Simulator' }}
        run: |
        cd VehicleConnectSDK
        # xcrun xctrace returns via stderr, not the expected stdout (see https://developer.apple.com/forums/thread/663959)
        device=`xcrun xctrace list devices 2>&1 | grep -oE 'iPhone.*?[^\(]+' | head -1 | awk '{$1=$1;print}' | sed -e "s/ Simulator$//"`
        if [ $scheme = default ]; then scheme=$(cat default); fi
        if [ "`ls -A | grep -i \\.xcworkspace\$`" ]; then filetype_parameter="workspace" && file_to_build="`ls -A | grep -i \\.xcworkspace\$`"; else filetype_parameter="project" && file_to_build="`ls -A | grep -i \\.xcodeproj\$`"; fi
        file_to_build=`echo $file_to_build | awk '{$1=$1;print}'`
        xcodebuild build-for-testing -scheme "$scheme" -"$filetype_parameter" "$file_to_build" -destination "platform=$platform,name=$device"
        - uses: actions/upload-artifact@v4
        with:
        name: VehicleConnectSDK-framework
        path: /Users/runner/Library/Developer/Xcode/DerivedData/VehicleConnectSDK-crfmbpmppqiclweufvtrmvjzodmo/Build/Products/Debug-iphonesimulator/VehicleConnectSDK.framework
```
### Build the App
- `iOSVehicleConnectApp` is written in Swift. It is compatible with iOS 16 and later and with iOS devices.
- The workflow is configured to run on `macos server` and uses an `ios simulator` to build the project.
- The `xcodebuild` tool is configured to generate the build artifacts.
- After a successful build, the artifacts are uploaded to the artifacts location of the run action

## Build the Android Mobile SDK and App using GitHub Actions
- The workflow is configured to set up the JDK version to Temurin distribution of Java 17.
- The workflow includes a step to run `gradle build` to package the artifacts.
- After a successful build, the `androidVehicleConnectSDK.aar` is uploaded to the artifacts location of the run action.
```xml
 steps:
    - uses: actions/checkout@v4
    - name: set up JDK 17
      uses: actions/setup-java@v3
      with:
        java-version: '17'
        distribution: 'temurin'
        cache: gradle

    - name: Grant execute permission for gradlew
      run: chmod +x gradlew
    - name: Build with Gradle
      run: ./gradlew build
        
    # Upload Artifact Build
    - name: Upload AAR - ${{ env.main_project_module }}
      uses: actions/upload-artifact@v3
      with:
      name: androidVehicleConnectSDK.aar
      path: androidVehicleConnectSDK/build/outputs/aar/
```

### Build the App
- `androidVehicleConnectApp` is written in Kotlin. It is compatible with Android 7.0 (API level 24) and later and with Android devices.
- The workflow is configured to set up the JDK version to Temurin distribution of Java 17.
- The workflow includes a step to run `gradle build` to package the artifacts.
- After a successful build, `vehicleConnectApp.apk` is uploaded to the artifacts location of the run action.

