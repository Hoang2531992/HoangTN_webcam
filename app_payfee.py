import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import cv2

import os
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["AC92740f266eb4575add6fd0d06763180f"]
auth_token = os.environ["fed65278e32a08bec2a3693e695cc55c"]
client = Client(account_sid, auth_token)

token = client.tokens.create()

st.title("My first Streamlit app")
st.write("Hello, world")


class VideoProcessor:
    def __init__(self) -> None:
        self.threshold1 = 100
        self.threshold2 = 200

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        img = cv2.cvtColor(cv2.Canny(img, self.threshold1, self.threshold2), cv2.COLOR_GRAY2BGR)

        return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    rtc_configuration={
        "iceServers": token.ice_servers
    }
)
if ctx.video_processor:
    ctx.video_processor.threshold1 = st.slider("Threshold1", min_value=0, max_value=1000, step=1, value=100)
    ctx.video_processor.threshold2 = st.slider("Threshold2", min_value=0, max_value=1000, step=1, value=200)
