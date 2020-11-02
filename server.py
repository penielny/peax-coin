from flask import Flask , render_template,request,session, redirect,url_for
from markupsafe import escape

from Blockchain import Chain

from Block import Block

from Account import Account

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
# setting up blockchain
chain = Chain()
g =Block(amount=2090.00008000,from_="Genesis",to_="Genesis",comment="welcome to peax-coin")
g.prev_hash = "0"*64
g.current_hash = "0"*chain.difficulty+"0"*(64-chain.difficulty)
chain.blocks.append(g)
print(" * [Blockchain sync]: Pulling blocks")
chain.sync()
print(" * [Blockchain sync]: Done")

# landing
@app.route("/")
def index():
	return render_template('index.html',session=session)

@app.route("/login",methods=["POST","GET"])
def login():
	if request.method == "POST":
		key = request.form.get('key')
		password = request.form.get('password')
		acc = Account(email=key ,password=password , private_key=key)
		# print(f"account validation : {acc.is_valid()}")
		if acc.is_valid():
			session['data'] = acc.get_info()
			return redirect(url_for('dashboard'))
	if session:
		return redirect(url_for('dashboard'))
	return render_template('login.html')

@app.route('/my',methods=["GET","POST"])
def dashboard():
	if session:
		acc= Account(private_key=session['data']['private_key'],password=session['data']['password'])
		transactions = [x for x in acc.transactions()]
		for x in acc.pendings():
			transactions.append(x)
		return render_template('dashboard.html',session=session['data'],transactions=transactions[:6],tl=len(transactions))
	return redirect(url_for('login'))

@app.route('/send',methods=["POST"])
def send():
	pxn_amount = request.form.get('pxn_amount')
	rcv_wallet = request.form.get('rcv_wallet')
	comment = request.form.get('comment')
	if not session:
		return redirect(url_for('index'))

	key = session['data']['private_key']
	password = session['data']['password']
	acc = Account(email=key ,password=password , private_key=key)
	if acc.is_valid():
		print(acc.send_pxn(ammount=float(pxn_amount), recv_wallet=rcv_wallet , comment=comment ,blockchain=chain))
		print(chain.pending_blocks)
		session['data'] = acc.get_info()
		return redirect(url_for('dashboard'))
	return redirect(url_for('login'))

@app.route('/create' , methods=["POST"])
def create():
	r_email = request.form.get('r_email')
	r_password = request.form.get('r_password')
	acc = Account(email=r_email ,password=r_password , private_key=r_email)
	if acc.validate():
		print("user already exist")
		return redirect(url_for('login'))
	acc.create()
	if acc.is_valid():
		session['data'] = acc.get_info()
		return redirect(url_for('dashboard'))
	print("problem creating account")
	return redirect(url_for('index'))

# dashboard[current price , exchange desk , transactions,buy and sell]
@app.route('/logout')
def logout():
    session.pop('data', None)
    return redirect(url_for('index'))

app.run(debug=True)