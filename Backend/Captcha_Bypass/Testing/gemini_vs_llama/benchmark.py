import os
import time
import csv
from setup import solve_with_gemini, solve_with_llama

image_dir = r"Backend\Captcha_Bypass\Testing\gemini_vs_llama\downloaded_captchas"
output_csv = r"Backend\Captcha_Bypass\Testing\gemini_vs_llama\captcha_comparison_results.csv"

results = []

for i in range(1, 26):
    image_path = os.path.join(image_dir, f"captcha_{i}.png")
    print(f"\n📸 Testing image {i}/25: {image_path}")

    try:
        g_start = time.time()
        gemini_result = solve_with_gemini(image_path)
        g_time = round(time.time() - g_start, 2)
    except Exception as e:
        gemini_result = f"ERROR: {e}"
        g_time = -1

    try:
        l_start = time.time()
        llama_result = solve_with_llama(image_path)
        l_time = round(time.time() - l_start, 2)
    except Exception as e:
        llama_result = f"ERROR: {e}"
        l_time = -1

    print(f"🤖 Gemini: {gemini_result} ({g_time}s)")
    print(f"🦙 LLaMA : {llama_result} ({l_time}s)")

    # Ask user which is correct
    correct = input("✅ Which is correct? (g=Gemini, l=LLaMA, b=Both, n=None): ").strip().lower()
    results.append([image_path, gemini_result, g_time, llama_result, l_time, correct])

# Save results to CSV
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Image", "Gemini_Output", "Gemini_Time", "LLaMA_Output", "LLaMA_Time", "Correct"])
    writer.writerows(results)

print(f"\n✅ Benchmark complete. Results saved to: {output_csv}")
