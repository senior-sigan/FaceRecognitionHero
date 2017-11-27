package org.senior_sigan.facerevolution

import com.google.android.gms.vision.face.Face

data class FaceWithEmotion(val face: Face, val emotion: String)