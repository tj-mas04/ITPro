import mss

with mss.mss() as sct:
    # Define monitor region: left, top, width, height
    monitor = {"top": 100, "left": 100, "width": 300, "height": 200}
    sct_img = sct.grab(monitor)

    # Save the image
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="region_capture.png")
