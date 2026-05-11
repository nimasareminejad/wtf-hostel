<!DOCTYPE html>
<!-- saved from url=(0034)https://hostel-app-4.onrender.com/ -->
<html lang="fa" dir="rtl"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    
    <link rel="stylesheet" href="./hostel-app-4.onrender.com_files/bootstrap.rtl.min.css">
    <style>
        body { font-family: tahoma; background: #f4f7f6; }
        .stat-box { background: white; padding: 20px; border-radius: 10px; border-bottom: 5px solid #222; }
        .bed { width: 165px; min-height: 145px; border-radius: 10px; border: 1px solid #ccc; display: inline-flex; flex-direction: column; align-items: stretch; justify-content: flex-start; cursor: pointer; margin: 5px; background: #fff; font-size: 11px; vertical-align: top; padding: 8px; line-height: 1.7; text-align: right; }
        .bed-empty { align-items: center; justify-content: center; text-align: center; min-height: 75px; }
        .occupied { background: #0d6efd; color: white; border: none; }
        .debtor { border: 3px solid #dc3545 !important; box-shadow: 0 0 0 2px rgba(220,53,69,.15); }
        .settled { border: 3px solid #198754 !important; }
        .bed-title { font-weight: bold; font-size: 12px; border-bottom: 1px solid rgba(255,255,255,.35); margin-bottom: 4px; padding-bottom: 3px; }
        .bed-row { display: flex; justify-content: space-between; gap: 6px; }
        .money { direction: ltr; unicode-bidi: plaintext; }
    </style>
</head>
<body class="modal-open" style="overflow: hidden; padding-right: 15px;">
    <nav class="navbar navbar-dark bg-dark mb-4 p-3">
        <div class="container-fluid">
            <span class="navbar-brand">سیستم حسابداری و مدیریت هاستل (نسخه Enterprise)</span>
            <div class="d-flex gap-2">
                <button class="btn btn-warning btn-sm" onclick="new bootstrap.Modal(document.getElementById(&#39;expM&#39;)).show()">ثبت هزینه (خرید/قبوض)</button>
                <a href="https://hostel-app-4.onrender.com/financial_report" class="btn btn-info btn-sm text-white">گزارش تراز مالی</a>
                <button class="btn btn-danger btn-sm" onclick="confirmReset()">ریست اضطراری</button>
                <a href="https://hostel-app-4.onrender.com/logout" class="btn btn-secondary btn-sm">خروج</a>
            </div>
        </div>
    </nav>

    <div class="container-fluid px-4">
        <div class="row g-3 mb-4">
            <div class="col-md-3"><div class="stat-box" style="border-color: #198754"><b>موجودی نقد صندوق:</b><br><h4>372,580</h4></div></div>
            <div class="col-md-3"><div class="stat-box" style="border-color: #dc3545"><b>کل هزینه‌ها:</b><br><h4>0</h4></div></div>
            <div class="col-md-3"><div class="stat-box" style="border-color: #0d6efd"><b>مطالبات (بدهی مشتریان):</b><br><h4>493,860</h4></div></div>
            <div class="col-md-3"><div class="stat-box" style="border-color: #ffc107"><b>سود خالص عملیاتی:</b><br><h4>372,580</h4></div></div>
        </div>

        <div class="row">
            
            <div class="col-md-6">
                <h5 class="p-2 bg-secondary text-white rounded">طبقه اول</h5>
                
                <div class="card p-3 mb-3 shadow-sm">
                    <div class="d-flex justify-content-between border-bottom pb-2 mb-2"><b>101 (خصوصی)</b> <small>VIP</small></div>
                    <div>
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(1)">
                                <div class="bed-title">سعید و شقایق</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">180,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">40,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">140,000</b></div>
                            </div>
                            
                        
                    </div>
                </div>
                
                <div class="card p-3 mb-3 shadow-sm">
                    <div class="d-flex justify-content-between border-bottom pb-2 mb-2"><b>102 (3 تخته)</b> <small>Standard</small></div>
                    <div>
                        
                            
                            <div class="bed occupied settled" onclick="openLedger(4)">
                                <div class="bed-title">ولادیمر</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-04</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">15,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">20,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">-5,000</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(2)">
                                <div class="bed-title">امیرارسلان شبانی س</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">75,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">57,500</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">17,500</b></div>
                            </div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(2, 3, 200000)">تخت 3<br>خالی</div>
                            
                        
                    </div>
                </div>
                
                <div class="card p-3 mb-3 shadow-sm">
                    <div class="d-flex justify-content-between border-bottom pb-2 mb-2"><b>103 (6 تخته)</b> <small>Standard</small></div>
                    <div>
                        
                            
                            <div class="bed occupied settled" onclick="openLedger(3)">
                                <div class="bed-title">فرشاد حسینی یک لنگ</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">79,980</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">79,980</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">0</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied settled" onclick="openLedger(5)">
                                <div class="bed-title">سلمان شادکامان</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-04</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">7,500</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">7,500</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">0</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(6)">
                                <div class="bed-title">محسن یوسفی</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">79,980</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">65,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">14,980</b></div>
                            </div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(3, 4, 150000)">تخت 4<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(3, 5, 150000)">تخت 5<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(3, 6, 150000)">تخت 6<br>خالی</div>
                            
                        
                    </div>
                </div>
                
                <div class="card p-3 mb-3 shadow-sm">
                    <div class="d-flex justify-content-between border-bottom pb-2 mb-2"><b>104 (10 تخته)</b> <small>Economy</small></div>
                    <div>
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(7)">
                                <div class="bed-title">فرهاد  محبتی</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">60,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">-9,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">69,000</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(8)">
                                <div class="bed-title">مهدی فرشباف اکبری</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">60,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">0</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">60,000</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(10)">
                                <div class="bed-title">ایوب ملکی پری</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">60,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">8,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">52,000</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(11)">
                                <div class="bed-title">علی مرادی </div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">75,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">-19,500</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">94,500</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(12)">
                                <div class="bed-title">علی گودرزی</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-02</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">2,500</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">0</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">2,500</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied settled" onclick="openLedger(13)">
                                <div class="bed-title">حامد کلانتری فرد</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-02</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">2,500</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">2,500</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">0</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(14)">
                                <div class="bed-title">وحید عیوضی</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-04-06</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">52,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">35,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">17,000</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(15)">
                                <div class="bed-title">مهدی مختاری</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-04-20</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">24,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">14,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">10,000</b></div>
                            </div>
                            
                        
                            
                            <div class="bed occupied settled" onclick="openLedger(16)">
                                <div class="bed-title">DU BOIS</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-03</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">8,000</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">8,000</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">0</b></div>
                            </div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(4, 10, 120000)">تخت 10<br>خالی</div>
                            
                        
                    </div>
                </div>
                
            </div>
            
            <div class="col-md-6">
                <h5 class="p-2 bg-secondary text-white rounded">طبقه دوم</h5>
                
                <div class="card p-3 mb-3 shadow-sm">
                    <div class="d-flex justify-content-between border-bottom pb-2 mb-2"><b>201 (پسرانه)</b> <small>Male</small></div>
                    <div>
                        
                            
                            <div class="bed occupied debtor" onclick="openLedger(9)">
                                <div class="bed-title">نیما صارمی نژاد</div>
                                <div class="bed-row"><span>ورود:</span><b>2026-05-01</b></div>
                                <div class="bed-row"><span>خروج:</span><b>2026-05-31</b></div>
                                <div class="bed-row"><span>قیمت کل:</span><b class="money">79,980</b></div>
                                <div class="bed-row"><span>پرداختی:</span><b class="money">63,600</b></div>
                                <div class="bed-row"><span>مانده:</span><b class="money">16,380</b></div>
                            </div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(5, 2, 180000)">تخت 2<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(5, 3, 180000)">تخت 3<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(5, 4, 180000)">تخت 4<br>خالی</div>
                            
                        
                    </div>
                </div>
                
                <div class="card p-3 mb-3 shadow-sm">
                    <div class="d-flex justify-content-between border-bottom pb-2 mb-2"><b>202 (دخترانه)</b> <small>Female</small></div>
                    <div>
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(6, 1, 180000)">تخت 1<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(6, 2, 180000)">تخت 2<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(6, 3, 180000)">تخت 3<br>خالی</div>
                            
                        
                            
                            <div class="bed bed-empty" onclick="openCheckin(6, 4, 180000)">تخت 4<br>خالی</div>
                            
                        
                    </div>
                </div>
                
            </div>
            
        </div>
    </div>

    <div class="modal fade" id="expM" tabindex="-1"><div class="modal-dialog"><form action="https://hostel-app-4.onrender.com/action/expense" method="POST" class="modal-content p-4">
        <h5>ثبت سند هزینه (خروجی)</h5>
        <input name="title" placeholder="بابت..." class="form-control mb-2" required="">
        <input name="amount" type="number" placeholder="مبلغ (تومان)" class="form-control mb-2" required="">
        <select name="cat" class="form-select mb-3"><option>قبوض</option><option>خرید مایحتاج</option><option>تعمیرات</option><option>پرسنل</option></select>
        <button class="btn btn-danger w-100">ثبت در دفتر روزنامه</button>
    </form></div></div>

    <div class="modal fade show" id="checkinModal" tabindex="-1" aria-modal="true" role="dialog" style="display: block;"><div class="modal-dialog"><form action="https://hostel-app-4.onrender.com/action/checkin" method="POST" class="modal-content p-4">
        <input type="hidden" name="rid" id="in_rid" value="2"><input type="hidden" name="bnum" id="in_bnum" value="3">
        <h5>پذیرش و افتتاح حساب</h5>
        <input name="name" placeholder="نام مسافر" class="form-control mb-2" required="">
        <input name="passport" placeholder="کد ملی / پاسپورت" class="form-control mb-2" required="">
        <div class="row g-2 mb-3">
            <div class="col-6"><label class="small">تاریخ ورود</label><input name="checkin" type="date" class="form-control" value="2026-05-01" required=""></div>
            <div class="col-6"><label class="small">تاریخ خروج</label><input name="checkout" type="date" class="form-control"></div>
            <div class="col-6"><label class="small">نرخ شبانه</label><input name="rate" id="in_rate" type="number" class="form-control" required=""></div>
            <div class="col-6"><label class="small">دریافت اول (بیعانه)</label><input name="pay" type="number" class="form-control" value="0"></div>
        </div>
        <button class="btn btn-primary w-100">صدور فاکتور و اسکان</button>
    </form></div></div>

    <div class="modal fade" id="ledgerModal" tabindex="-1"><div class="modal-dialog modal-lg"><div class="modal-content p-4" id="ledgerBody"></div></div></div>

    <script src="./hostel-app-4.onrender.com_files/bootstrap.bundle.min.js.download"></script>
    <script>
        function confirmReset() { if(confirm("هشدار: تمام اطلاعات حسابداری و مسافران پاک خواهد شد!")) window.location.href="/action/reset"; }
        function openCheckin(rid, bnum, rate) {
            document.getElementById('in_rid').value=rid; document.getElementById('in_bnum').value=bnum; document.getElementById('in_rate').value=rate;
            new bootstrap.Modal(document.getElementById('checkinModal')).show();
        }
        function toman(n) { return Number(n || 0).toLocaleString(); }

        async function openLedger(bid) {
            const r = await fetch('/api/guest/' + bid); const d = await r.json();
            let html = `<div class="d-flex justify-content-between align-items-start gap-3">
                <div>
                    <h4>صورتحساب: ${d.g.name}</h4>
                    <div class="text-muted">کد ملی / پاسپورت: ${d.g.passport || '-'}</div>
                </div>
                <h4 class="${d.balance > 0 ? 'text-danger' : 'text-success'}">${toman(d.balance)} مانده</h4>
            </div>

            <div class="row g-2 my-3">
                <div class="col-md-3"><div class="border rounded p-2 bg-light"><small>تاریخ ورود</small><br><b>${d.g.checkin}</b></div></div>
                <div class="col-md-3"><div class="border rounded p-2 bg-light"><small>تاریخ خروج</small><br><b>${d.summary.checkout_display}</b></div></div>
                <div class="col-md-3"><div class="border rounded p-2 bg-light"><small>تعداد شب</small><br><b>${d.summary.nights}</b></div></div>
                <div class="col-md-3"><div class="border rounded p-2 bg-light"><small>نرخ شبانه</small><br><b>${toman(d.summary.rate)}</b></div></div>
                <div class="col-md-4"><div class="border rounded p-2"><small>قیمت کل آن بازه</small><br><b>${toman(d.summary.total)}</b></div></div>
                <div class="col-md-4"><div class="border rounded p-2"><small>جمع پرداختی</small><br><b class="text-success">${toman(d.summary.paid)}</b></div></div>
                <div class="col-md-4"><div class="border rounded p-2"><small>باقی‌مانده پرداختی</small><br><b class="${d.balance > 0 ? 'text-danger' : 'text-success'}">${toman(d.balance)}</b></div></div>
            </div>

            <div style="max-height:300px; overflow-y:auto" class="border p-2 my-3 bg-light">
                <table class="table table-sm"><thead><tr><th>تاریخ</th><th>شرح</th><th>نوع</th><th>مبلغ</th></tr></thead>
                <tbody>${d.l.map(t => `<tr><td>${t.date}</td><td>${t.desc}</td><td>${t.type == 'DEBIT' ? 'بدهکار' : 'بستانکار'}</td><td class="${t.type=='DEBIT'?'text-danger':'text-success'}">${toman(t.amount)}</td></tr>`).join('')}</tbody>
                </table>
            </div>
            <form action="/action/pay" method="POST" class="input-group mb-3">
                <input type="hidden" name="bid" value="${d.g.id}"><input name="amount" type="number" class="form-control" placeholder="مبلغ پرداختی مشتری..." required>
                <button class="btn btn-success">ثبت دریافت نقد</button>
            </form>
            <div class="d-flex gap-2"><button onclick="window.print()" class="btn btn-outline-dark w-100">چاپ فاکتور</button>
            <a href="/action/checkout/${d.g.id}" class="btn btn-danger w-100" onclick="return confirm('تصفیه نهایی؟')">تصفیه و خروج نهایی</a></div>`;
            document.getElementById('ledgerBody').innerHTML = html; new bootstrap.Modal(document.getElementById('ledgerModal')).show();
        }
    </script>

<div class="modal-backdrop fade show"></div></body></html>
