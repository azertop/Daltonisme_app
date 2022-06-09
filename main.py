import streamlit as st
from streamlit_option_menu import option_menu
import cv2
import PIL.Image as im
import numpy as np
from streamlit_webrtc import webrtc_streamer, RTCConfiguration,WebRtcMode
import av
from streamlit_image_comparison import image_comparison

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
# class VideoProcessor:
#     def recv(self, frame):
#         img = frame.to_ndarray(format="rgb24")
#         if bleu :
#             img = daltonisme(img,"bleu")
#         if rouge :
#             img = daltonisme(img,"rouge")
#         if vert:
#             img = daltonisme(img,"vert")
#         return av.VideoFrame.from_ndarray(img, format="rgb24")

st.title("Simulateur de daltonisme")

# with st.sidebar :
#     choice = st.selectbox("Image",["Image","Webcam"])
#     bleu = st.checkbox("Bleu")
#     rouge = st.checkbox("Rouge")
#     vert = st.checkbox("Vert")
st.write("## Type de daltonisme :")
choices = st.multiselect("", ["Deutéranopie (Vert)","Protanopie (Rouge)","Tritanopie (Bleu)"])  
    

def daltonisme(img,type:str) :
    lms_matrix = np.array(
        [[0.3904725 , 0.54990437, 0.00890159],
        [0.07092586, 0.96310739, 0.00135809],
        [0.02314268, 0.12801221, 0.93605194]]
        )
    img = np.tensordot(img, lms_matrix, axes=([2], [1]))
    if type == "rouge":
        sim_matrix = np.array([[0, 0.90822864, 0.008192], [0, 1, 0], [0, 0, 1]], dtype=np.float16)
    elif type == "bleu":
        sim_matrix = np.array([[1, 0, 0], [0, 1, 0], [-0.15773032,  1.19465634, 0]], dtype=np.float16)
    elif type =="vert":
        sim_matrix =  np.array([[1, 0, 0], [1.10104433,  0, -0.00901975], [0, 0, 1]], dtype=np.float16)
    else : 
        return None    
    img = np.tensordot(img, sim_matrix, axes=([2], [1]))
    rgb_matrix = np.array(
        [[ 2.85831110e+00, -1.62870796e+00, -2.48186967e-02],
        [-2.10434776e-01,  1.15841493e+00,  3.20463334e-04],
        [-4.18895045e-02, -1.18154333e-01,  1.06888657e+00]]
        )
    img = np.tensordot(img, rgb_matrix, axes=([2], [1])).astype(np.uint8)
    return img    

# if choice == "Webcam":
#     st.subheader("Simulation Webcam")
#     webrtc_streamer(key="example",mode=WebRtcMode.SENDRECV, media_stream_constraints={"video": True, "audio": False}, rtc_configuration=RTC_CONFIGURATION
#     )
#elif choice == "Image":

img = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
if img != None:
    img = im.open(img)
    img = img.convert('RGB')
    img = np.array(img)
    img1 = np.array(img)
    if "Tritanopie (Bleu)" in choices :
        img1 = daltonisme(img,"bleu")
        st.write("Blavla")
    if "Protanopie (Rouge)" in choices :
        img1 = daltonisme(img,"rouge")
    if "Deutéranopie (Vert)" in choices:
        img1 = daltonisme(img,"vert")
    image_comparison(img1=img,img2=img1)    