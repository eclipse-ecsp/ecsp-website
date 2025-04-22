# Table of Contents

This section describes the various backend Cloud components as part of the Eclipse CSP and how to develop and build them.

1. [Overview](#overview)
2. [List of Libraries](#list-of-libraries)
3. [Build Guidelines](#build-guidelines)

## Overview

Our custom libraries are published as artifacts to [Maven central repository](https://repo1.maven.org/maven2/org/eclipse/ecsp/).

## List of Libraries

- Our libraries are currently published to GitHub Packages.
- To use our libraries, you need to add the dependency in your `pom.xml` file.
- The libraries are written in `Java`.
- The libraries are built and packaged using the `Maven` build tool

The following table describes the Eclipse CSP libraries.

| Library Name          | Description                                                                                                                                                                                                                                                                                                                                                                            | Repository Link                                                  | Package Link                                                                   |
|:----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------|:-------------------------------------------------------------------------------|
| utils                 | Provides centralized logging, health checks, diagnostic data reporting and application metrics such ad counters, gauges and histograms                                                                                                                                                                                                                                                 | [Link](https://github.com/eclipse-ecsp/utils)                    | [Link](#available-soon) |
| sql-dao               | Provides HikariCP pooled connections to the Postgres DB and manages database lifecycle                                                                                                                                                                                                                                                                                                 | [Link](https://github.com/eclipse-ecsp/sql-dao)                  | [Link](#available-soon) |
| nosql-dao             | Provides base interface to perform MongoDB related queries                                                                                                                                                                                                                                                                                                                             | [Link](https://github.com/eclipse-ecsp/nosql-dao)                | [Link](#available-soon) |
| stream-base           | Provides a layer of abstraction for kafka-streams processing mechanism                                                                                                                                                                                                                                                                                                                 | [Link](#available-soon)                                          | [Link](#available-soon) |
| redis-cache           | Provides Redis server backed caching capabilities                                                                                                                                                                                                                                                                                                                                      | [Link](#available-soon)                                          | [Link](#available-soon) |
| transformers          | Provides serialization/deserialization capabilities                                                                                                                                                                                                                                                                                                                                    | [Link](https://github.com/eclipse-ecsp/transformers)             | [Link](#available-soon) |
| entities              | Provides abstraction for event specifications and centralises common entities. Provides support for related commmon functionalities like Serialization, Automatic auditing of entities, retries, event lifecycle hooks and mappings                                                                                                                                                    | [Link](https://github.com/eclipse-ecsp/entities)                 | [Link](#available-soon) |
| api-common            | Provides common and necessary functionalities required to expose rest APIs. It exposes common REST based tasks related to health monitors, metrics, JSON support functions and push message to Kafka cluster etc                                                                                                                                                                       | [Link](#available-soon)                                          | [Link](#available-soon) |
| services-common       | Provides following common and necessary functionalities required to enable stream processors - Authentication token, Connected Personal Account, StolenVehicle, PrivacyMode, SettingsManager, VehicleProfile, Custom Codec for MongoDB, Json Utils                                                                                                                                     | [Link](#available-soon)                                          | [Link](#available-soon) |
| services-dependencies | Provides functionality to manage versions of internal and third-party dependencies.                                                                                                                                                                                                                                                                                                    | [Link](#available-soon)                                          | [Link](#available-soon) |
| api-registry-common   | Provides common functionalities to enable api gateway                                                                                                                                                                                                                                                                                                                                  | [Link](https://github.com/eclipse-ecsp/api-gateway)              | [Link](#available-soon) |

NOTES:

- Refer the the `README` file in the `Repository Link` column of each row for more information about each library.
- Refer the `Package Link` in the table above to get the latest version of the library

## Build Guidelines

&nbsp;&nbsp;&nbsp;&nbsp;Refer the [build_guidelines.md](build_guidelines.md) for more information about how to build the libraries
