import numpy as np


def _make_homogeneous_rep_matrix(R, t):
    P = np.zeros((4, 4))
    P[:3, :3] = R
    P[:3, 3] = t.reshape(3)
    P[3, 3] = 1
    return P


# direct linear transform
def DLT(P1, P2, point1, point2):

    A = [
        point1[1] * P1[2, :] - P1[1, :],
        P1[0, :] - point1[0] * P1[2, :],
        point2[1] * P2[2, :] - P2[1, :],
        P2[0, :] - point2[0] * P2[2, :],
    ]
    A = np.array(A).reshape((4, 4))
    # print('A: ')
    # print(A)

    B = A.transpose() @ A
    from scipy import linalg

    U, s, Vh = linalg.svd(B, full_matrices=False)

    # print('Triangulated point: ')
    # print(Vh[3,0:3]/Vh[3,3])
    return Vh[3, 0:3] / Vh[3, 3]


def read_camera_parameters(camera_id, savefolder="../posefit/python/bodypose3d/camera_parameters/"):

    cmtx = np.loadtxt(savefolder + "c" + str(camera_id) + "_mtx.dat")
    dist = np.loadtxt(savefolder + "c" + str(camera_id) + "_dist.dat")

    return cmtx, dist


def read_rotation_translation(camera_id, savefolder="../posefit/python/bodypose3d/camera_parameters/"):

    rot = np.loadtxt(savefolder + "c" + str(camera_id) + "_rot.dat")
    trans = np.loadtxt(savefolder + "c" + str(camera_id) + "_trans.dat")

    return rot, trans


def _convert_to_homogeneous(pts):
    pts = np.array(pts)
    if len(pts.shape) > 1:
        w = np.ones((pts.shape[0], 1))
        return np.concatenate([pts, w], axis=1)
    else:
        return np.concatenate([pts, [1]], axis=0)


def get_projection_matrix(camera_id):

    # read camera parameters
    cmtx, dist = read_camera_parameters(camera_id)
    rvec, tvec = read_rotation_translation(camera_id)

    # calculate projection matrix
    P = cmtx @ _make_homogeneous_rep_matrix(rvec, tvec)[:3, :]
    return P


def write_keypoints_to_disk(filename, kpts):
    fout = open(filename, "w")

    for frame_kpts in kpts:
        for kpt in frame_kpts:
            if len(kpt) == 2:
                fout.write(str(kpt[0]) + " " + str(kpt[1]) + " ")
            else:
                fout.write(str(kpt[0]) + " " + str(kpt[1]) + " " + str(kpt[2]) + " ")

        fout.write("\n")
    fout.close()


if __name__ == "__main__":

    P2 = get_projection_matrix(0)
    P1 = get_projection_matrix(1)
