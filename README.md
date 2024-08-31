# 👁️ سیگما-بی 🏦

سیگما-بی مجموعه ای از پروتکل ها و ابزار های رمزنگاری است که ارائه ***«اثبات خصوصی اندوخته»*** و یا ***«Private Proof of Reserves»*** را برای صرافی های متمرکز رمزارز ممکن می‌کند. «خصوصی» بودن سیگما-بی از درز پیدا کردن آدرس های صرافی و کاربران صرافی و داده های مالی مربوط به صرافی (نظیر مقدار کل بدهی) جلوگیری می‌کند. این سند به فلسفه پشت پروتکل سیگما-بی و جزئیات فنی آن می‌پردازد.

## نحوه استفاده

کاربران می‌توانند با استفاده از افزونه کروم/فایرفاکس سیگما-بی، فرایند صحت‌سنجی اثبات‌های ارائه شده توسط صرافی‌ها را انجام دهند. افزونه‌های منتشر شده از کلیدهای صحت‌سنجی شماره `0015` ([لیست مشارکت‌ها](https://github.com/nobitex/sigmab-trusted-setup)) استفاده می‌کنند.

### طریقه نصب روی مرورگر کروم

1. ابتدا [sigmab-chrome.zip](https://github.com/nobitex/sigmab/releases/download/v0.1.0/sigmab-chrome.zip) را دانلود کنید.
1. به صفحه Chrome Extensions بروید.
3. از قسمت بالا-راست صفحه، گزینه Developer-Mode را فعال کنید.
4. فایل `sigmab-chrome.zip` را بر روی صفحه افزونه‌ها درگ-اند-دراپ کنید.

### طریقه نصب روی مرورگر فایرفاکس

1. ابتدا [sigmab-firefox.zip](https://github.com/nobitex/sigmab/releases/download/v0.1.0/sigmab-firefox.zip) را دانلود کنید.
1. به صفحه Add-ons and themes بروید.
2. بر روی دکمه چرخ‌دنده ⚙️ کلیک کرده و سپس گزینه Debug Add-ons را انتخاب کنید.
3. دکمه Load temporary Add-on را بزنید.
4. فایل `sigmab-firefox.zip` را در این بخش انتخاب کنید.

پس از نصب افزونه سیگما-بی، می‌توانید اثبات اندوخته خود را از وبسایت صرافی دریافت کرده و آن را صحت‌سنجی کنید!

## اثبات اندوخته چیست؟

اثبات اندوخته، صرافی های متمرکز (امانی) را قادر می‌سازد که به کاربران خود اثبات کنند که ***به اندازه بدهی خود به کاربران، اندوخته دارند.*** در پروتکل های اثبات اندوخته فعلی، دو چیز اثبات می‌شود:

1. صرافی به اندازه $`n`$ واحد پولی اندوخته دارد.
2. مجموع بدهی های صرافی به کاربران از $`n`$ کوچکتر است.

***برای اثبات قسمت اول***، صرافی ها چاره ای ندارند جز اینکه آدرس کیف پول های خود را بطور عمومی افشا کنند. کاربران می‌توانند با بررسی موجودی داخل این آدرس ها و جمع زدن آنها، مقدار $`n`$ را بدست بیاورند. **سیگما-بی راه حل نوینی را ارائه می‌کند که صرافی ها بتوانند بدون افشا کردن آدرس های خود، به کاربران ثابت کنند که صاحب $`n`$ واحد پولی هستند.**

***برای اثبات قسمت دوم***، فرض کنید نوبیتکس لیستی در اختیار دارد که هر سطر آن حاوی شناسه کاربر و موجودی کیف پول امانی او می‌شود. این لیست را «لیست بدهی» می‌نامیم. نوبیتکس می‌تواند این لیست را به طور عمومی منتشر کند. کاربران می‌توانند لیست را مشاهده کرده، و از حضور خود در این لیست مطمئن شوند. پس از اطمینان حاصل کردن از حضور خود در لیست، کاربران می‌توانند مجموع دارایی های همه کاربران در لیست (بدهی کل) را محاسبه کرده و مطمئن شوند که این مقدار، از اندوخته صرافی (مقدار $`n`$) کوچکتر است.

- اگر مقدار بدهی ها از مقدار اندوخته ها بزرگتر باشد نوبیتکس واضحا در اثبات اندوخته خود شکست خورده است.
- اگر نام شما در لیست موجود نباشد، بدین معنی است که نوبیتکس بدهی شما را در نظر نگرفته و این احتمال وجود دارد که نوبیتکس به اندازه بدهی خود به کاربران اندوخته نداشته باشد.

*(نکته: کاربران همچنین باید مطمئن شوند که لیست بدهی اعلامی نوبیتکس در یک تاریخ معین، همواره ثابت است و نوبیتکس در هر بار استعلام تغییری در آن ایجاد نمی‌کند. در غیر این صورت نوبیتکس می‌تواند یکبار لیست حاوی نام شما را منتشر کند و بعد از متقاعد کردن شما، نام شما را از لیست حذف کند و نام شخص دیگری را به جای شما گذاشته و او را نیز متقاعد کند)*

## حریم خصوصی لیست بدهی
واضحا انتشار عمومی لیست بدهی ها غیرقابل انجام است چرا که به حریم خصوصی کاربران نوبیتکس آسیب جدی وارد می‌کند. در صورت عمومی شدن لیست بدهی، همه کاربران می‌توانند موجودی رمزارزی همه کاربران را ببینند.

### تابع درهم‌سازی
تابع درهم‌سازی، یک تابع ریاضیاتی است که یک ورودی با اندازه دلخواه می‌گیرد و همواره یک خروجی با اندازه ثابت تحویل می‌دهد. این تابع همچنین ویژگی های زیر را دارد:

- کوچکترین تغییر در ورودی باعث تغییر شگرف در خروجی می‌شود.
- پیدا کردن ورودی از روی خروجی بسیار سخت و ناممکن است.

### تعهد رمزی

فرض کنید آتوسا و بابک میخواهند پشت تلفن «سنگ-کاغذ-قیچی» بازی کنند. متاسفانه همواره این امکان وجود دارد که بابک، در حین اینکه آتوسا انتخاب خود را فریاد میزند، سریعا انتخاب او را شنیده و انتخاب خود را با توجه به انتخاب آتوسا اعلام کند و همواره برنده شود. بابک می‌تواند تاخیر در اعلام انتخاب خود را گردن تاخیر صدا در تلفن بیاندازد.

با توجه به یک‌طرفه بودن توابع درهم‌سازی امن، آتوسا و بابک می‌توانند بدون اینکه داده ای را افشا کند، به آن داده متعهد شوند. مثال:

آتوسا و بابک می‌توانند به جای اینکه انتخاب خود را فریاد بزنند، از انتخاب های خود Hash بگیرند و با اعلام این مقدار به یکدیگر، به انتخاب های خود متعهد شوند. پس از رد و بدل کردن تعهد ها، آتوسا و بابک می‌توانند انتخاب اصلی خود را با آرامش کامل اعلام کرده و برنده مشخص می‌شود. همچنین، آتوسا و بابک پس از شنیدن انتخاب های اصلی، می‌توانند با Hash گرفتن از آنها و مقایسه نتیجه با تعهد های قبلی، از پایبند بودن یکدیگر به تعهد های خود مطمئن شوند. در صورتی که هرکس از تعهد خود سرپیچی کند، بازنده اعلام می‌شود.

### اثبات دانش-صفر
فرض کنید که $`f`$ تابعی است که چند ورودی میگیرد و یک خروجی می‌دهد. اثبات‌های دانش-صفر، پروتکل های رمزنگاری هستند که ما را قادر می‌سازند ثابت کنیم ورودی هایی را می‌دانیم که در صورت اعمال $`f`$ روی آنها، خروجی برابر یک مقدار خاص می‌شود. با استفاده از اثبات‌های دانش-صفر و تعهد های رمزی، می‌توانیم نوعی «لیست بدهی خصوصی» طراحی کنیم.

### لیست بدهی خصوصی
فرض کنید که بجای انتشار عمومی لیست بدهی، از آن Hash میگیریم و آن را انتشار می‌دهیم. با اینکار به لیست بدهی متعهد می‌شویم. حال فرض کنید که تابع $`f_1`$ با مشخصات زیر داریم:

‍‍
$`f_1(L, i) = (h(L), \sum_{k}{L[k]_{balance}}, L[i]_{id}, L[i]_{balance})`$


این تابع لیست بدهی ($`L`$) و یک اندیس ($`i`$) را به عنوان ورودی دریافت می‌کند و یک چهارتایی را به عنوان خروجی برمی‌گرداند:

- $`h(L)`$ هش لیست بدهی است.
- $`\sum_{k}{L[k]_{balance}}`$ مجموع همه بدهی های موجود در لیست است.
- $`L[i]_{id}`$ شناسه $`i`$-امین کاربر موجود در لیست بدهی است.
- $`L[i]_{balance}`$ موجودی $`i`$-امین کاربر موجود در لیست بدهی است.


حال فرض کنید که نوبیتکس ابتدا لیست بدهی $`L`$ را با توجه به لیست کاربران خود می‌سازد و هش آن را ($`C=h(L)`$) بصورت عمومی منتشر میکند. سپس با استفاده از اثبات‌های دانش-صفر ثابت می‌کند که ورودی هایی را برای تابع $`f_1`$ می‌داند که باعث خروجی $`(C,T,K,V)`$ می‌شود. در صورت برابر بودن $`C`$ خروجی با $`C`$ اولیه اعلام شده توسط نوبیتکس، عملا نوبیتکس ثابت کرده است که:

- اولا: مجموع موجودی های کاربران برابر $`T`$ است.
- دوما: شخصی داخل لیست وجود دارد که شناسه او برابر $`K`$ است.
- سوما: موجودی همان شخص داخل لیست برابر $`V`$ است.

آتوسا با دریافت این اثبات و بررسی برابر بودن $`C`$ با تعهد لیست بدهی ها که نوبیتکس از قبل اعلام کرده بود، قانع می‌شود که هنگام متعهد شدن نوبیتکس به لیست بدهی، آتوسا (با شناسه $`K`$) و $`V`$ واحد رمزارز او نیز در نظر گرفته شده اند. همچنین آتوسا متوجه می‌شود که مقدار کل بدهی اعلامی نوبیتکس برابر $`T`$ است.

آتوسا می‌تواند مقدار $`T`$ را با مقدار کل اندوخته های نوبیتکس (که $`n`$ است) مقایسه کند.

## خصوصی سازی اندوخته های نوبیتکس

همانطور که پیش از این گفته شد، نقطه قوت سیگما-بی نسبت به سایر پروتکل ها، قابلیت آن در اثبات اندوخته (قسمت اول) بدون فاش کردن آدرس های صرافی است.

### بلاکچین های Account-based

بیتکوین، به عنوان اولین رمزارزی که تکنولوژی بلاکچین را معرفی کرد، از معماری UTXO پیروی می‌کند. در این معماری، اشخاص، صاحب «حساب» های بیتکوینی نیستند. بلکه صاحبه «سکه» هایی هستند که می‌توانند به سکه های کوجکتر و با صاحب های متفاوت شکسته شوند. در این مدل، یک نفر می‌تواند با شکستن سکه خود به دو سکه کوچکتر، پرداخت بیتکوینی انجام دهد. یکی از این دو سکه باید به نام شخص دریافت‌کننده سکه، و دیگری باقی‌مانده پرداخت و به نام شخص پرداخت‌کننده خواهد بود.

پس از بیتکوین، بلاکچین های دیگری معرفی شدند که از معماری دیگری استفاده می‌کردند: به جای اینکه اشخاص صاحب سکه های با ارزش های متفاوت باشند، هر شخص داخل پروتکل صاحب حسابی است که مقدار موجودی آن با دریافت و پرداخت هایی که انجام می‌دهد تغییر می‌کند. هر حساب نیز به یک کلید عمومی متصل است. 

### لیست موجودی خصوصی
برخی از بلاکچین های Account-based (مثل اتریوم)، در بلوک های خود، هش کل اکانت‌های موجود نیز اعلام می‌کنند. این مقدار تحت عنوان stateRoot منتشر می‌شود. می‌توان این مقدار را تعهدی بر لیست موجودی های همه اکانت‌های اتریومی در نظر گرفت.

تابع $`f_2`$ با مشخصات زیر را در نظر بگیرید:

$`f_2(A,i,sig) = (h(A), A[i]_{balance}, verifySig(A[i]_{pubkey}, \text{"I am Nobitex!"}, sig))`$


این تابع لیست کلید‌عمومی و موجودی **کل** اکانت‌های اتریومی ($`A`$)، یک اندیس ($`i`$) و یک امضا ($`sig`$) را به عنوان ورودی دریافت می‌کند و یک سه‌تایی را به عنوان خروجی برمی‌گرداند:

- $`h(A)`$ هش لیست موجودی کل اکانت‌های اتریومی .
- $`A[i]_{balance}`$ موجودی $`i`$-امین اکانت 
- $`verifySig(A[i]_{pubkey}, \text{"I am Nobitex!"}, sig)`$ یک مقدار بولینی نشان‌دهنده اینکه آیا اکانت $`i`$-ام به درستی پیام $`\text{"I am Nobitex!"}`$ را امضا کرده است یا نه (با نوجه به $`sig`$)

اثبات موفق دانایی ورودی های مناسب برای تابع $`f_2`$ به طوری که ۳ تایی $(C, B, 1)$ را برگرداند بدین معنی است که:

* امضایی را می‌دانیم که نشان می‌دهد صاحب یکی از اکانت‌های داخل اتریوم هستیم، و مقدار موجودی این اکانت برابر $`B`$ است.

البته همچنین باید اطمینان حاصل کنیم که مقدار $`C`$ دقیقا برابر با همان مقداری است که توسط نود های اتریومی تحت عنوان stateRoot منتشر شده است.

حال نوبیتکس می‌تواند چند اثبات تولید کند و هر اثبات نشان دهد که نوبیتکس صاحب $`B_i`$ واحد رمزارز است. کاربران می‌توانند مقادیر موجودی های اثبات شده را با یکدیگر جمع بزنند تا موجودی کل نوبیتکس را بدست بیاورند و در آخر چک کنند که این مقدار از مقدار بدهی های نوبیتکس بیشتر باشد.

### اکانت‌های تکراری

پروتکل توصیف شده در حال حاضر یک مشکل جدی دارد. نوبیتکس می‌تواند برای یکی از اکانت‌های خود اثبات‌های متعدد تولید کند و ادعا کند که موجودی ها مربوط به اکانت‌های مختلف هستند. از آنجایی که آدرس اکانت ها مخفی است، راهی برای تشخیص تکراری نبودن اکانت ها وجود ندارد. یک راه‌حل مبتکرانه برای حل این مشکل وجود دارد. فرض کنید که تابع $`f_2`$ را به شکل زیر تغییر می‌دهیم:

$`f_2(A,i,sig,salt) = (h(A), A[i]_{balance}, verifySig(A[i]_{pubkey}, \text{"I am Nobitex!"}, sig), h(A[i]_{pubkey}, salt))`$

به ورودی های تابع یک مقدار $`salt`$ اضافه می‌کنیم و در خروجی‌ها نیز مقدار $`h(A[i]_{pubkey}, salt)`$ را برمیگردانیم. واضح است که این مقدار برای هر کلید عمومی یک مقدار ثابت است (نمی‌توان اثبات‌های مختلف برای یک کلیدعمومی ثابت با $`f_2`$ ساخت بطوری که چهارمین خروجی تابع متفاوت باشد). این مقدار باعث می‌شود که بتوانیم اکانت‌های تکراری را تشخیص دهیم.

با توجه به ویژگی های توابع درهم‌سازی، نمی‌توان از روی $`h(A[i]_{pubkey}, salt)`$ به $`A[i]_{pubkey}`$ رسید (اگر $`salt`$ یک مقدار رندوم باشد). بنابراین با اینکه جلوی کلیدعمومی های تکراری را می‌گیریم، کلیدعمومی همچنان محرمانه باقی می‌ماند. البته این به شرطی است که مقدار salt خصوصی بماند ولی مطمئن باشیم مقدار $`salt`$ استفاده شده بین همه اثبات‌ها یکسان باشد. برای این منظور می‌توانیم یک تعهد رمزی از $`salt`$ نیز در خروجی ها داشته باشیم:

$`f_2(A,i,sig,salt) = (h(A), A[i]_{balance}, verifySig(A[i]_{pubkey}, \text{"I am Nobitex!"}, sig), h(A[i]_{pubkey}, salt), h(salt))`$

### خصوصی سازی موجودی ها

اگر دقت کرده باشید، در این پروتکل با اینکه آدرس های صرافی را مخفی کرده ایم، همچنان مقدار کل دارایی نوبیتکس لو میرود. دلایل متعددی می‌تواند وجود داشته باشد که نوبیتکس نخواهد مقدار کل دارایی خود را فاش کند. دقیقا همانطور که در قسمت قبلی کلیدعمومی را به صورت رمزی شده فاش کردیم، میتوانیم موجودی را نیز به صورت رمز شده فاش کنیم. کافی است در خروجی دوم، بجای $`A[i]_{balance}`$، مقدار $`h(A[i]_{balance},salt)`$ را برگردانیم.

در صورت انجام این کار، کاربری که اثبات‌ها را صحت‌سنجی می‌کند دیگر نمی‌تواند مجموع موجودی ها را بدست آورد، چرا که آنها مقادیر رمزی‌شده هستند. می‌توانیم یک تابع سوم $`f_3`$ داشته باشیم که ثابت کند: مجموع مقدار رمزی شده $`a`$ و $`b`$ برابر مقدار رمزی‌شده $`a+b`$ است:

$`f_3(a,b,salt) = (h(a, salt), h(b, salt), h(a + b, salt))`$

با استفاده از اثبات‌های متعدد روی $`f_3`$ می‌توانیم ثابت کنیم که مجموع کل دارایی های نوبیتکس برابر با مقدار رمزی شده $`B_{encoded}`$ است.

حال فرض کنید که در لیست بدهی نیز بجای فاش کردن مقدار کل بدهی بصورت مستقیم، با همین رویکرد، مقدار رمزی‌شده کل بدهی را برگردانیم، با یک تابع چهارمی، از بزرگتر بودن مقدار رمزی‌شده دارایی از مقدار رمزی‌شده بدهی مطمئن شویم. در این صورت ***نوبیتکس می‌تواند ثابت کند که به اندازه بدهی های خود اندوخته دارد، بدون آنکه مقدار اندوخته و یا مقدار بدهی خود را فاش کند.***


## راه‌اندازی امن

متاسفانه قبل از اینکه بتوان از پروتکل های دانش-صفر zkSNARKs برای تولید اثبات استفاده کرد، می‌بایست یکسری «پارامتر های اولیه» طی فرایندی که از آن با عنوان Trusted-Setup یاد می‌شود تولید شوند. ***این فرایند باید حتما توسط چند شخص مستقل انجام شود. اگر پارامتر های اولیه تنها توسط یک نفر تولید شوند، امکان تولید اثبات‌های تقلبی توسط آن شخص وجود دارد.***

### زباله های سمی

در طی فرایند مشارکت در تولید پارامتر های اولیه، داده هایی تولید می‌شوند که حتما باید پس از مشارکت از بین بروند. ***برای اینکه پروتکل امن باشد، تنها کافی است که یکی از شرکت‌کننده ها زباله های سمی خود را از بین ببرد.*** اثبات‌های تقلبی تنها درصورتی قابل تولید هستند که همه‌ی ‌شرکت کننده ها به عمد زباله های سمی خود را نگه دارند و با مشارکت همدیگر اثبات‌ها را بسازند. احتمال چنین موقعیتی بسیار ناچیز است، مگر اینکه تعداد شرکت‌کننده ها کم باشد. شرکت کننده های این فرایند می‌توانند برای اطمینان بیشتر از لو نرفتن زباله های سمی، تولید پارامتر ها را در یک کامپیوتر ایزوله (و حتی داخل یک قفسه فارادی) انجام دهند!

### شرکت کننده ها

لیست افرادی که در فرایند راه‌اندازی امن سیگما-بی شرکت کرده اند:

- [کیوان کامبخش](https://github.com/keyvank) 
- [محمدعلی حیدری ](https://github.com/ostadgeorge)
- [پردیس طولابی](https://github.com/toolabi)
- [حمید باطنی](https://github.com/irnb)
- [علیرضا مفتخر](https://github.com/alirezamft)
- [امیرحسین آذرپور](https://github.com/AmirH-A)
- [امیرحسین حسنینی](https://github.com/am1rh0ss3in)
- [امیرعلی آذرپور](https://github.com/amalaz)
- [محمد سهراب ثامنی](https://github.com/sohrabsameny)
- [نیما یزدان مهر](https://github.com/n1rna)
- [پریسا حسنی زاده](https://github.com/parizad1188)
- [شهریار ابراهیمی](https://github.com/lovely-necromancer)
- [ سیاوش تفضلی](https://github.com/SiavashTafazoli)
- [پدرام میرشاه](https://github.com/itsspedram)
- [عباس آشتیانی](https://github.com/abbasashtiani)
- [علی مقصودی](https://github.com/Alitelepromo)
- [آرش فتاح‌زاده](https://github.com/iRhonin)
- [امید مسگرها](https://github.com/armagg)

دور ریختن زباله ها سمی حتی توسط یکی از این افراد باعث می‌شود اطمینان حاصل کنیم که تولید اثبات‌های جعلی امکان‌پذیر نیست.

