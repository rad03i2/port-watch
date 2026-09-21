# Port Watch

A small, dependency-free TCP port availability monitor for developers, homelabs, CI checks, and local service diagnostics.

Port Watch answers a deliberately narrow question: **can a TCP connection be established to this host and port right now?** It can perform one-shot checks or repeatedly watch a bounded list of ports and report state transitions.

## English

### Why it exists
Developers often need a simple health check without a heavyweight monitoring stack. Port Watch uses Python's standard library, installs as a normal CLI, returns useful exit codes, and can emit machine-readable JSON.

### Features
- Check one port, a comma-separated list, or ranges such as `8000-8005`.
- Watch ports continuously and report open/closed transitions.
- Connection latency for successful probes.
- Newline-delimited JSON in watch mode for scripts and log pipelines.
- `--only-open` for concise interactive output.
- Bounded input: at most 256 distinct ports per invocation.
- Configurable connection timeout and watch interval.
- Reusable Python API.
- No runtime dependencies, telemetry, accounts, credentials, or cloud service.
- Cross-platform CI for Linux, Windows, and macOS.

### Requirements
- Python 3.10+
- TCP networking permitted by the local OS/firewall

### Installation
```bash
git clone https://github.com/rad03i2/port-watch.git
cd port-watch
python -m pip install -e .
```

For development:
```bash
python -m pip install -e . pytest
```

### Usage
Check a local web service:
```bash
port-watch 127.0.0.1 8000
```

Check several ports:
```bash
port-watch localhost 22,80,443,8000-8003
```

Watch for changes every 10 seconds:
```bash
port-watch localhost 3000,5432,6379 --watch --interval 10
```

Run exactly five watch cycles as JSON:
```bash
port-watch localhost 8000,8080 --watch --count 5 --json
```

Show only open ports:
```bash
port-watch localhost 3000-3010 --only-open
```

Exit codes for one-shot checks: `0` means every requested port was open, `1` means at least one was closed/unreachable, and `2` means invalid input. `Ctrl+C` in watch mode exits with `130`.

### Python API
```python
from port_watch import parse_ports, probe_many

results = probe_many("localhost", parse_ports("80,443"), timeout=0.5)
for result in results:
    print(result.port, result.open, result.latency_ms)
```

### Configuration
Port Watch intentionally has no config file or environment variables. Runtime behavior is explicit through CLI options. This reduces hidden state and makes CI usage reproducible.

### Project structure
```text
src/port_watch/
  __init__.py   Public API
  core.py       Parsing, TCP probes, change detection, watch loop
  cli.py        Command-line interface
tests/          Unit and local socket integration tests
.github/workflows/ci.yml
```

### Testing
```bash
python -m compileall -q src tests
pytest -q
port-watch --version
```

The integration test opens an ephemeral listener on `127.0.0.1`; it does not contact an Internet host.

### Preview / screenshot guidance
For a portfolio screenshot, run a local development server and show `port-watch localhost 3000,8000 --watch`. Do not publish screenshots containing private IP addresses, internal hostnames, or sensitive infrastructure details.

### Security and privacy
Use Port Watch only against systems you own or have explicit authorization to test. It performs TCP connection attempts only: no authentication, service fingerprinting, payload delivery, or exploitation. The 256-port input limit is intentional. There is no telemetry. JSON logs can contain hostnames/IP addresses, so protect them when they identify private infrastructure.

### Limitations
- TCP only; UDP is not supported.
- A successful TCP handshake does not prove that the application behind the port is healthy.
- Checks are sequential, prioritizing predictable low-impact behavior over scan speed.
- DNS resolution and firewall behavior can affect results.
- State is in-memory only; restarting watch mode resets transition history.
- This is not a replacement for a full monitoring/alerting platform.

### Optional roadmap
Potential future work: opt-in persistence for state history, configurable notification adapters, and application-level HTTP/TLS health checks. These are not implemented today.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Security guidance is in [SECURITY.md](SECURITY.md).

### License
MIT — see [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

## العربية

### نظرة عامة
**Port Watch** أداة خفيفة لمراقبة توفر منافذ TCP للمطورين والبيئات المحلية وعمليات CI وتشخيص الخدمات. تجيب عن سؤال محدد: هل يمكن إنشاء اتصال TCP مع هذا المضيف والمنفذ الآن؟ ويمكنها إجراء فحص واحد أو مراقبة مجموعة محدودة من المنافذ وإظهار تغير حالتها.

### لماذا المشروع؟
أحيانًا يحتاج المطور إلى التحقق من تشغيل خدمة محلية أو قاعدة بيانات أو خادم تطوير دون تثبيت منصة مراقبة كبيرة. تعتمد الأداة على مكتبة Python القياسية فقط، وتوفر رموز خروج واضحة وJSON مناسبًا للأتمتة.

### الميزات
- فحص منفذ واحد أو قائمة أو نطاق مثل `8000-8005`.
- مراقبة متكررة وإظهار الانتقال بين مفتوح ومغلق.
- قياس زمن الاتصال الناجح بالميلي ثانية.
- إخراج JSON قابل للمعالجة البرمجية.
- خيار `--only-open` لعرض المنافذ المفتوحة فقط.
- حد أقصى 256 منفذًا مختلفًا في التشغيل الواحد.
- مهلة اتصال وفاصل مراقبة قابلان للضبط.
- واجهة Python قابلة لإعادة الاستخدام.
- لا توجد تبعيات تشغيل خارجية أو Telemetry أو حسابات أو مفاتيح API.

### المتطلبات والتثبيت
يتطلب Python 3.10 أو أحدث.
```bash
git clone https://github.com/rad03i2/port-watch.git
cd port-watch
python -m pip install -e .
```

للتطوير والاختبار:
```bash
python -m pip install -e . pytest
pytest -q
```

### أمثلة الاستخدام
```bash
port-watch 127.0.0.1 8000
port-watch localhost 22,80,443,8000-8003
port-watch localhost 3000,5432 --watch --interval 10
port-watch localhost 8000,8080 --watch --count 5 --json
```

في الفحص الواحد: الرمز `0` يعني أن كل المنافذ المطلوبة مفتوحة، و`1` يعني وجود منفذ مغلق أو غير قابل للوصول، و`2` يعني خطأ في الإدخال.

### الإعداد والبنية
لا تستخدم الأداة ملف إعداد أو متغيرات بيئة؛ جميع الخيارات صريحة في CLI لتقليل الحالة المخفية. يوجد المحرك في `src/port_watch/core.py`، وواجهة الأوامر في `cli.py`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`.

### الاختبارات
```bash
python -m compileall -q src tests
pytest -q
port-watch --version
```
اختبار الشبكة يفتح منفذًا مؤقتًا على `127.0.0.1` فقط ولا يتصل بخادم على الإنترنت.

### إرشادات المعاينة
لصورة Portfolio يمكن تشغيل خدمة تطوير محلية ثم عرض أمر المراقبة في الطرفية. تجنب نشر صور تحتوي على عناوين IP خاصة أو أسماء مضيفين داخلية أو تفاصيل بنية حساسة.

### الأمان والخصوصية
استخدم الأداة فقط على الأنظمة التي تملكها أو لديك تصريح صريح لفحصها. الأداة تحاول إنشاء اتصال TCP فقط ولا تنفذ تسجيل دخول أو استغلالًا أو بصمة للخدمة أو إرسال حمولة تطبيقية. لا توجد Telemetry. قد تتضمن سجلات JSON أسماء مضيفين أو عناوين IP، لذلك تعامل معها كبيانات حساسة عند الحاجة.

### القيود
- TCP فقط ولا يوجد UDP.
- نجاح اتصال TCP لا يضمن سلامة التطبيق نفسه.
- الفحص تسلسلي ومصمم ليكون منخفض التأثير وليس ماسحًا سريعًا.
- DNS والجدار الناري قد يؤثران في النتائج.
- سجل تغير الحالة يبقى في الذاكرة فقط أثناء التشغيل.
- ليست بديلًا عن منصات المراقبة والتنبيه المتكاملة.

### تطوير اختياري مستقبلًا
يمكن مستقبلًا إضافة حفظ اختياري لسجل الحالة وتنبيهات قابلة للتهيئة وفحوص HTTP/TLS على مستوى التطبيق. هذه الميزات غير منفذة حاليًا.

### المساهمة والترخيص
راجع [CONTRIBUTING.md](CONTRIBUTING.md) للمساهمة و[SECURITY.md](SECURITY.md) لإرشادات الأمان. المشروع مرخص بترخيص MIT الموجود في [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
