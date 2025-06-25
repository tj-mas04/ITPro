import mss

with mss.mss() as sct:
    # Define monitor region: left, top, width, height
    monitor = {"top": 900, "left": 600, "width": 120, "height": 40}
    sct_img = sct.grab(monitor)

    # Save the image
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="region_capture.png")
