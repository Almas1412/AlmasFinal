# AlmasFinal
Final Project for ENU

Это моя дипломная работа. Система безналичной оплаты для магазинов. Используется Python, PyQT, Arduino и Android

Файлы для корректного запуска файла Shopui.py рекомендуется запустить Файл sketch_may14a.ino на Arduino для подачи данных на сериний порт и
положить файл cart2.ui вместе с файлом Shopui.py в одну папку. Рекемендуется использовать среду программирования PyCharm для быстрой настройки библеотек

Мобильное приложение приведено в папке nexus с папкой ресурсов. Так же рекемендуется запустить в среде Android Studio

файл gradle приведу ниже, нужно для настройки firebase


****************************************************************************************************
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
    id 'com.google.gms.google-services'
}

android {
    compileSdk 32

    defaultConfig {
        applicationId "com.example.nexus"
        minSdk 21
        targetSdk 32
        versionCode 1
        versionName "1.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
    kotlinOptions {
        jvmTarget = '1.8'
    }
    buildFeatures {
        viewBinding true
    }
}

dependencies {


    implementation 'com.google.zxing:core:3.4.0'
    implementation 'androidx.core:core-ktx:1.7.0'
    implementation 'androidx.appcompat:appcompat:1.4.2'
    implementation 'com.google.android.material:material:1.6.1'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    implementation 'androidx.annotation:annotation:1.2.0'
    implementation 'androidx.lifecycle:lifecycle-livedata-ktx:2.3.1'
    implementation 'androidx.lifecycle:lifecycle-viewmodel-ktx:2.3.1'
    implementation platform('com.google.firebase:firebase-bom:30.1.0')
    implementation 'com.google.firebase:firebase-database-ktx'
    implementation 'com.google.firebase:firebase-auth-ktx:21.0.5'
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.3'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.4.0'

}
****************************************************************************************************
