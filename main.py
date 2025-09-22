import os
import argparse
import cv2


def read_text(file_path):
    """Membaca file teks dan menampilkan isinya."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"[TEKS] Isi file:\n{content}")
    except Exception as e:
        print(f"Error membaca teks: {e}")


def read_image(file_path):
    """Membaca gambar dan menampilkan informasi ukuran + preview."""
    try:
        img = cv2.imread(file_path)
        if img is None:
            raise ValueError("Format gambar tidak dikenali.")
        height, width = img.shape[:2]
        channels = img.shape[2] if img.ndim == 3 else 1
        print(f"[GAMBAR] Resolusi: {width}x{height}, Channel: {channels}")

        # Preview gambar
        cv2.imshow("Preview Gambar", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error membaca gambar: {e}")


def read_video(file_path):
    """Membaca video dan menampilkan informasi durasi + resolusi."""
    try:
        cap = cv2.VideoCapture(file_path)
        if not cap.isOpened():
            raise ValueError("Video tidak bisa dibuka.")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frames / fps if fps > 0 else 0

        print(f"[VIDEO] Resolusi: {width}x{height}, FPS: {fps:.2f}, Frame: {frames}, Durasi: {duration:.2f}s")

        # Tampilkan beberapa frame pertama
        count = 0
        while cap.isOpened() and count < 30:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Preview Video", frame)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                break
            count += 1

        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error membaca video: {e}")


# def main():



# if __name__ == "__main__":
#     main()

parser = argparse.ArgumentParser(description="Program baca data (teks, gambar, video)")
parser.add_argument("file", help="Path ke file yang ingin dibaca")
args = parser.parse_args()

file_path = args.file
if not os.path.exists(file_path):
    print("File tidak ditemukan.")
    return

ext = os.path.splitext(file_path)[1].lower()

if ext in [".txt", ".md"]:
    read_text(file_path)
elif ext in [".jpg", ".jpeg", ".png", ".bmp"]:
    read_image(file_path)
elif ext in [".mp4", ".avi", ".mov", ".mkv"]:
    read_video(file_path)
else:
    print("Format file belum didukung.")
