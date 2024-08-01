import com.android.build.gradle.tasks.MergeSourceSetFolders
import org.jetbrains.kotlin.gradle.tasks.KotlinJvmCompile

plugins {
    alias(libs.plugins.androidApplication)
    alias(libs.plugins.jetbrainsKotlinAndroid)
}

val skikoNativeX64: Configuration by configurations.creating
val skikoNativeArm64: Configuration by configurations.creating
val jniDir = "${projectDir.absolutePath}/src/main/jniLibs"
val unzipTaskX64 = tasks.register("unzipNativeX64", Copy::class) {
    destinationDir = file("$jniDir/x86_64")
    from(skikoNativeX64.map { zipTree(it) }) {
        include("*.so")
    }
    includeEmptyDirs = false
}
val unzipTaskArm64 = tasks.register("unzipNativeArm64", Copy::class) {
    destinationDir = file("$jniDir/arm64-v8a")
    from(skikoNativeArm64.map { zipTree(it) }) {
        include("*.so")
    }
    includeEmptyDirs = false
}

tasks.withType<MergeSourceSetFolders>().configureEach {
    dependsOn(unzipTaskX64)
    dependsOn(unzipTaskArm64)
}

tasks.withType<KotlinJvmCompile>().configureEach {
    dependsOn(unzipTaskX64)
    dependsOn(unzipTaskArm64)
}


android {
    namespace = "com.am.alekscompphys"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.am.alekscompphys"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        vectorDrawables {
            useSupportLibrary = true
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = "11"
    }

    buildFeatures {
        compose = true
    }

    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.1"
    }

    packaging {
        resources {
            pickFirsts += listOf(
                "META-INF/AL2.0",
                "META-INF/LGPL2.1",
                "META-INF/ASL-2.0.txt",
                "META-INF/LICENSE.md",
                "META-INF/NOTICE.md",
                "META-INF/LGPL-3.0.txt",
            )
            excludes += listOf(
                "META-INF/kotlin-jupyter-libraries/libraries.json",
                "META-INF/{INDEX.LIST,DEPENDENCIES}",
                "{draftv3,draftv4}/schema",
                "arrow-git.properties",
                "license/*",
                "/META-INF/{AL2.0,LGPL2.1}",
                "META-INF/ASL-2.0.txt",
                "META-INF/LICENSE.md",
                "META-INF/NOTICE.md",
                "META-INF/LGPL-3.0.txt",
                "META-INF/LICENSE-EDL-1.0.txt",
                "LICENSE-EDL-1.0.txt",
                "*/LICENSE-EDL-1.0.txt"
            )
        }
    }
}

dependencies {

    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.lifecycle.runtime.ktx)
    implementation(libs.androidx.activity.compose)
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.ui)
    implementation(libs.androidx.ui.graphics)
    implementation(libs.androidx.ui.tooling.preview)
    implementation(libs.androidx.material3)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation(libs.androidx.ui.test.junit4)
    debugImplementation(libs.androidx.ui.tooling)
    debugImplementation(libs.androidx.ui.test.manifest)
    implementation("org.jetbrains.skiko:skiko-android:0.7.92")
    skikoNativeX64("org.jetbrains.skiko:skiko-android-runtime-x64:0.7.92")
    skikoNativeArm64("org.jetbrains.skiko:skiko-android-runtime-arm64:0.7.92")
    implementation("org.jetbrains.lets-plot:lets-plot-kotlin-kernel:4.6.0")
    implementation("org.jetbrains.lets-plot:lets-plot-common:4.3.0")
    implementation("org.jetbrains.lets-plot:lets-plot-compose:1.0.3")
    implementation("org.jetbrains.kotlinx:kandy-lets-plot:0.6.0") {
        exclude(group = "commons-logging", module = "commons-logging")
        exclude(group = "org.jetbrains.lets-plot", module = "lets-plot-kotlin-jvm")
        exclude(group = "io.swagger", module= "swagger-parser-safe-url-resolver")
        exclude(group = "org.eclipse.collections", module = "eclipse-collections")
    }
    implementation("org.jetbrains.kotlinx:kotlin-statistics-jvm:0.2.1") {
        exclude(group = "commons-logging", module = "commons-logging")
        exclude(group = "org.jetbrains.lets-plot", module = "lets-plot-kotlin-jvm")
        exclude(group = "io.swagger", module= "swagger-parser-safe-url-resolver")
        exclude(group = "org.eclipse.collections", module = "eclipse-collections")
    }
}

