var express = require('express'),
	app = express(),
	path = require('path');

app.use('/public', express.static('public'))
app.use('/robots', express.static('robots'))

app.get('/', function(req,res){
    res.sendFile(path.join(__dirname + '/index.html'));
});

var server = require('http').Server(app),
	io = require('socket.io')(server),
	cIo = require('socket.io-client')('http://localhost:3001');
		
cIo.on('init', function (data) {
	console.log(data);
});

io.on('connection', function (socket) {
	socket.emit('init', 'Connected to bot server!');
	
	socket.on('f', function (data) {
		console.log('f');
		cIo.emit('forward', data);
	});
	
	socket.on('b', function (data) {
		console.log('b');
		cIo.emit('backward', data);
	});
	
	socket.on('r', function (data) {
		console.log('r');
		cIo.emit('right', data);
	});
	
	socket.on('l', function (data) {
		console.log('l');
		cIo.emit('left', data);
	});
	
	socket.on('shootR', function (data) {
		cIo.emit('shootR', data);
	});
	
	socket.on('shootL', function (data) {
		cIo.emit('shootL', data);
	});
	
	socket.on('missleR', function (data) {
		cIo.emit('missleR', data);
	});
	
	socket.on('missleL', function (data) {
		cIo.emit('missleL', data);
	});
});

server.listen(3000, function () {
	console.log('Robot API on port 3000')
});
