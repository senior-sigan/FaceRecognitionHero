package org.senior_sigan.facerevolution

import com.google.android.gms.vision.Detector
import com.google.android.gms.vision.Tracker
import com.google.android.gms.vision.face.Face
import org.senior_sigan.facerevolution.ui.camera.FaceGraphic
import org.senior_sigan.facerevolution.ui.camera.GraphicOverlay

/**
 * Face tracker for each detected individual. This maintains a face graphic within the app's
 * associated face overlay.
 */
class GraphicFaceTracker(
        private val mOverlay: GraphicOverlay?
) : Tracker<Face>() {
    private val mFaceGraphic: FaceGraphic = FaceGraphic(mOverlay)

    /**
     * Start tracking the detected face instance within the face overlay.
     */
    override fun onNewItem(faceId: Int, item: Face) {
        mFaceGraphic.setId(faceId)
    }

    /**
     * Update the position/characteristics of the face within the overlay.
     */
    override fun onUpdate(detectionResults: Detector.Detections<Face>, face: Face) {
        mOverlay?.add(mFaceGraphic)
        mFaceGraphic.updateFace(face)
    }

    /**
     * Hide the graphic when the corresponding face was not detected.  This can happen for
     * intermediate frames temporarily (e.g., if the face was momentarily blocked from
     * view).
     */
    override fun onMissing(detectionResults: Detector.Detections<Face>) {
        mOverlay?.remove(mFaceGraphic)
    }

    /**
     * Called when the face is assumed to be gone for good. Remove the graphic annotation from
     * the overlay.
     */
    override fun onDone() {
        mOverlay?.remove(mFaceGraphic)
    }
}