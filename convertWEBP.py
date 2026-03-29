import time

path = input("Enter the path to the folder containing images: ").strip().strip('"')
print("Starting conversion...")
start_time = time.time()
for i in range(100):
    print(f"Converting image {i + 1}...")
    time.sleep(0.1)  # Simulate time taken to convert an image
end_time = time.time()
print(f"Conversion completed in {end_time - start_time:.2f} seconds.")