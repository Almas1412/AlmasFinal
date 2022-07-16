package com.example.nexus

import com.google.firebase.database.Exclude
import com.google.firebase.database.IgnoreExtraProperties

@IgnoreExtraProperties
data class UserLogin(
    var id: String? = "",
    var name: String? = "",
    var email: String? = "",

    ) {

    @Exclude
    fun toMap(): Map<Any?, Any?> {
        return mapOf(
            "id" to id,
            "name" to name,
            "email" to email,

        )
    }
}