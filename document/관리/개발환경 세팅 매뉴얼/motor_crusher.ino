const int in1Pin = 10;
const int in2Pin = 9;

const long crushTime = 30000;//리니어 액츄에이터가 움직이는 동안 소요되는 최대시간 : 상수 정의



void setup() {
	//라즈베리파이 GPIO핀 세팅 
	pinMode(in1Pin, OUTPUT);
	pinMode(in2Pin, OUTPUT);

	crush();
}


//액츄에이터 정방향 동작 시작(열기)
void crush() {
	digitalWrite(in1Pin, LOW);
	digitalWrite(in2Pin, HIGH);
	delay(crushTime);
}

//액추에이터 역방향 동작(닫기)
void reverse() {
	digitalWrite(in1Pin, HIGH);
	digitalWrite(in2Pin, LOW);
	delay(crushTime);
}

//액츄에이터 동작 멈춤
void stop() {
	digitalWrite(inlPin, LOW);
	digitalWrite(in2Pin, LOW);
}