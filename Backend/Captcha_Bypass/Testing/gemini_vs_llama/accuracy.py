import csv

csv_path = r"Backend\Captcha_Bypass\Testing\gemini_vs_llama\captcha_comparison_results.csv"

# Counters
total = 0
gemini_correct = 0
llama_correct = 0
both_correct = 0
none_correct = 0

gemini_times = []
llama_times = []

gemini_failures = 0
llama_failures = 0

with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        total += 1

        g_output = row["Gemini_Output"].strip()
        l_output = row["LLaMA_Output"].strip()
        g_time = float(row["Gemini_Time"])
        l_time = float(row["LLaMA_Time"])
        correct = row["Correct"].strip().lower()

        # Accuracy
        if correct == "g":
            gemini_correct += 1
        elif correct == "l":
            llama_correct += 1
        elif correct == "b":
            both_correct += 1
        elif correct == "n":
            none_correct += 1

        # Failure count (empty or error output)
        if g_output.startswith("ERROR") or not g_output:
            gemini_failures += 1
        else:
            gemini_times.append(g_time)

        if l_output.startswith("ERROR") or not l_output:
            llama_failures += 1
        else:
            llama_times.append(l_time)

# Summary
print("\n === CAPTCHA Benchmark Summary ===\n")
print(f"Total Samples: {total}\n")

print("Accuracy (based on manual marking):")
print(f"  - Gemini correct       : {gemini_correct} ({(gemini_correct / total) * 100:.2f}%)")
print(f"  - LLaMA correct        : {llama_correct} ({(llama_correct / total) * 100:.2f}%)")
print(f"  - Both correct         : {both_correct} ({(both_correct / total) * 100:.2f}%)")
print(f"  - None correct         : {none_correct} ({(none_correct / total) * 100:.2f}%)\n")

print("Average Response Time:")
print(f"  - Gemini: {sum(gemini_times)/len(gemini_times):.2f}s" if gemini_times else "  - Gemini: No valid responses")
print(f"  - LLaMA : {sum(llama_times)/len(llama_times):.2f}s" if llama_times else "  - LLaMA : No valid responses\n")

print("Failure Count (empty or error responses):")
print(f"  - Gemini: {gemini_failures}")
print(f"  - LLaMA : {llama_failures}")

print(f"-> Gemini Accuracy : {((gemini_correct + both_correct) / total) * 100:.2f}%")
print(f"-> LLaMA Accuracy  : {((llama_correct + both_correct) / total) * 100:.2f}%")
