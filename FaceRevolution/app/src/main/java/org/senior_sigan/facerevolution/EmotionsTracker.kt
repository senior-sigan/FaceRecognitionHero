package org.senior_sigan.facerevolution

import android.util.Log
import com.google.android.gms.vision.Detector
import com.google.android.gms.vision.Tracker

class EmotionsTracker : Tracker<FaceWithEmotion>() {
    private val TAG = "EmotionsTracker"

    override fun onUpdate(
            detectionResults: Detector.Detections<FaceWithEmotion>,
            face: FaceWithEmotion
    ) {
        Log.i(TAG, "$face")
    }
}