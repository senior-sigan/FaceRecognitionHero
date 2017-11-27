package org.senior_sigan.facerevolution

import android.util.Log
import android.util.SparseArray
import com.google.android.gms.vision.Detector
import com.google.android.gms.vision.Frame
import com.google.android.gms.vision.face.Face

class EmotionsDetector(
        private val delegate: Detector<Face>
) : Detector<FaceWithEmotion>() {
    private val TAG = "EmotionsDetector"

    override fun detect(frame: Frame): SparseArray<FaceWithEmotion> {
        val faces = delegate.detect(frame)
        if (faces.size() == 0) return SparseArray(0)

        val face = faces.valueAt(0) ?: return SparseArray(0) // TODO: get the biggest image

        val borders = getBorders(face)
        val arr = frame.grayscaleImageData.array()

        // TODO: convert arr to matrix and get submatrix due to borders + some epsilon

        // TODO: send this matrix to the neural network

        // TODO: put this info to the Face? or another object

//        Log.i(TAG, "FACE: $borders, ${frame.metadata.width}, ${frame.metadata.height}, ${frame.metadata.rotation}")
        val result = SparseArray<FaceWithEmotion>(faces.size())
        (0 until faces.size())
                .map { faces.valueAt(it) }
                .forEach { result.put(it.id, FaceWithEmotion(it, "None")) }
        return result
    }

    override fun isOperational(): Boolean = delegate.isOperational
    override fun setFocus(p0: Int): Boolean = delegate.setFocus(p0)

    data class Borders(val left: Float, val right: Float, val top: Float, val bottom: Float)

    private fun getBorders(face: Face): Borders {
        val xOffset = face.width / 2.0f
        val yOffset = face.height / 2.0f
        val x = face.position.x + xOffset
        val y = face.position.y + yOffset
        val left = x - xOffset
        val top = y - yOffset
        val right = x + xOffset
        val bottom = y + yOffset
        return Borders(left, right, top, bottom)
    }
}