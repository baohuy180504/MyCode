#include <Servo.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
//Adafruit_SSD1306 display(128, 64, &Wire, -1);
#define OLED_RESET 4
Adafruit_SSD1306 display(OLED_RESET);

int count_R = 0;
int count_G = 0;
int count_B = 0;
int count_T = 0;

Servo myservo;

void setup()
{
  Serial.begin(115200);

  // Khởi tạo màn hình OLED
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.display();
  // Set chân và góc servo
  myservo.attach(5);
  myservo.write(50);

  delay(1000);
}

void loop()
{
  String data = "";
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    data += c;
    delay(2);
  }
  data.trim();
  if (data != "")
  {
    if (data == "R")
    {
      count_R += 1;
      //if (count_R > prev_count_R)
        myservo.write(50);
        //delay(5);
    }

    if (data == "G")
    {
      count_G += 1;
      //if (count_G > prev_count_G)
        myservo.write(100);
        //delay(5);
    }

    if (data == "B")
    {
      count_B += 1;
      //if (count_B > prev_count_B)
        myservo.write(150);
        //delay(5);
    }
    data = "";
  }

  // Cập nhật giá trị trạng thái trước đó
  //prev_count_R = count_R;
  //prev_count_G = count_G;
  //prev_count_B = count_B;
  count_T = count_R + count_G + count_B;
  updateDisplay();
}

void displayOLED()
{
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);

  display.setCursor(0, 0);
  display.print("HE THONG PHAN LOAI");

  display.setCursor(0, 10);
  display.print("RED: ");
  display.print(count_R);

  display.setCursor(60, 10);
  display.print("GREEN: ");
  display.print(count_G);

  display.setCursor(0, 25);
  display.print("BLUE: ");
  display.print(count_B);

  display.setCursor(60, 25);
  display.print("TOTAL: ");
  display.print(count_T);

  display.display();
}

void updateDisplay()
{
  displayOLED();
}
