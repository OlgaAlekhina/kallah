const BOTTOM_PLAYER = 0;
const TOP_PLAYER = 1;

// Функция возвращает номер лунки, в которую попадет последний камень, взятый из лунки well 
function lastWell(well)
{
	var nWell = Number(well.id);
	var nStones = Number(well.innerHTML);
	
	if( nWell < 6 )
		return (nWell + nStones)%13;
	else
		if((nWell - 7 + nStones)%13 < 7)
			return (nWell - 7 + nStones)%13 + 7;
		else
			return (nWell - 7 + nStones)%13 - 7;
}

// Функция добавляет лункам стороны nSide обработчики мыши и класс доступности.
// Параметры: nSide (0, 1) - сторона, first (true, false) - начало игры.
function initSide(nSide, first=false)
{
	document.querySelectorAll(getStrSide(nSide)).forEach(the_well => {
		// Если это первый ход - первая лунку неактивна. Пустые лунки неактивны.
		if((!first || Number(the_well.id) != 0) && Number(the_well.innerHTML) > 0)
		{
			the_well.addEventListener('click', handleWellClick);
			the_well.addEventListener('mouseenter', handleWellMouseenter);
			the_well.addEventListener('mouseleave', handleWellMouseleave);
			the_well.classList.add('my_turn');
			the_well.classList.remove('last_well');
		}
	});
}

// Функция удаляет из всех лунок обработчики мыши и класс доступности.
function cleanBoard()
{
	document.querySelectorAll('[data-cell]').forEach(the_well => {
		the_well.removeEventListener('click', handleWellClick);
		the_well.removeEventListener('mouseenter', handleWellMouseenter);
		the_well.removeEventListener('mouseleave', handleWellMouseleave);
		the_well.classList.remove('my_turn');
		the_well.classList.remove('last_well');
	});
}

// Функция заполняет все лунки 6-ю камнями, очищает калахи и активирует сторону пользователя.
function startGame()
{
	document.querySelectorAll('[class^="well"]').forEach(the_well => {
		the_well.innerHTML = 6;
	});

	document.querySelectorAll('[class^="kalakh"]').forEach(the_well => {
		the_well.innerHTML = 0;
	});
	
	cleanBoard();

	initSide(0, true);
	
	setMessage("Let's roll!");
}

function handleWellMouseenter(e)
{
	const well = e.target;
	document.getElementById(lastWell(e.target).toString(10)).classList.add('last_well');
}

function handleWellMouseleave(e)
{
	document.getElementById(lastWell(e.target).toString(10)).classList.remove('last_well');
}


async function handleWellClick(e)
{
	//Инактивирует лунки игрока
	cleanBoard();
	
	//Делает ход из выбранной лунки
	var nEndWell = await makeMove(Number(e.target.id));

	level = Array.from(document.getElementById("level_result").innerHTML)[0];
    console.log(level);
    let well_list = [];
    for(var i = 0; i < 14; i++){
        well_list.push(document.getElementById(i).innerHTML);
    }
    console.log(well_list)
    const socket = io();
    socket.emit('test', {well_list, level});
    socket.on('best_move', function(data) {
        console.log(data);
    });
	
	//Если последний камень НЕ попал в свой калах
	if( nEndWell != 6 )
	{
		//Компьютер делает ходы
		do
		{
			//Вызов асинхронной функции хода компьютера
			nEndWell = await computersTurn();
		}
		//пока последний камень попадает в его калах
		while( nEndWell == 13 );
	}
	
	//Активирует лунки игрока
	initSide(BOTTOM_PLAYER);
}

//Асинхронная функция хода компьютера
async function computersTurn()
{
	var nWell = 0; // Просто для примера
	
	//**********************************************************
	// Код запрашивающий ход у бэкенда и присваивающий его nWell
	//**********************************************************
	
	var nEndWell = await makeMove(nWell + 7);
	
	//Возвращает promise со значением resolve равным номеру последней ячейки
	return Promise.resolve(nEndWell);
}


async function makeMove(nWell)
{
	const elementList = document.querySelectorAll('[data-cell]');
	
	var clickSound = document.getElementById("click_sound");
	var grabSound = document.getElementById("grab_sound");
	
	
	var nCurrentWell = nWell;
	var nStones = Number(elementList[nCurrentWell].innerHTML);
	elementList[nCurrentWell].innerHTML = 0;
	var nKalakhIndex = (nCurrentWell < 6)?6:13;
	
	while(nStones--)
	{
		// Переходим в следующую лунку.
		nCurrentWell++;

		// Если попали в чужой калах, переходим в следующую лунку.
		if( nCurrentWell == (nKalakhIndex == 6?13:6) )
			nCurrentWell++;

		// Движемся по кругу. Если дошли до конца - начинаем сначала.
		if( nCurrentWell == 14 )
			nCurrentWell = 0;

		// Увеличиваем число камней на 1 в очередной лунке.
		elementList[nCurrentWell].innerHTML = Number(elementList[nCurrentWell].innerHTML) + 1;
		clickSound.play();
		//Задержка, равная длительности звука
		await sleep(clickSound.duration*1000); //clickSound.duration*1000);
	}	

	// Если последний камень попал в пустую лунку на стороне, с которой был сделан ход...	
	if( Number(elementList[nCurrentWell].innerHTML) == 1 && (( nCurrentWell < 6 && nWell < 6) || ( nCurrentWell > 6 && nWell > 6)) && nCurrentWell != 13 ) 
	{
		// Находим индекс противолежащей лунки.
		var nOppositWell = 12 - nCurrentWell;
		// Если в ней есть камни ...
		if( Number(elementList[nOppositWell].innerHTML) > 0 )
		{
			// Переносим их и камни из последней лунки в калах игрока, делавшего ход.
			elementList[nKalakhIndex].innerHTML = Number(elementList[nKalakhIndex].innerHTML) + 1 + Number(elementList[nOppositWell].innerHTML);
			elementList[nCurrentWell].innerHTML = 0;
			elementList[nOppositWell].innerHTML = 0;
			grabSound.play();
			//Задержка, равная длительности звука
			await sleep(grabSound.duration*1000);
		}
		
	}
	
	document.getElementById("info").innerHTML = Number(elementList[6].innerHTML) - Number(elementList[13].innerHTML);
	await sleep(500);
	
	//Возвращает promise со значением resolve равным номеру последней ячейки
	return Promise.resolve(nCurrentWell);
}

//Функция возвращает сторону лунки well.
function getSide( well )
{
	return Number(well.id) < 7 ? BOTTOM_PLAYER : TOP_PLAYER;
}

//Функция возвращает строку классов стороны nSide.
function getStrSide( nSide )
{
	return nSide==BOTTOM_PLAYER ? '[class^="well_H"]' : '[class^="well_C"]';
}

//Функция возвращает калах стороны nSide.
function getKalakh( nSide )
{
	return nSide == BOTTOM_PLAYER ? "6" : "13";
}

//Функция возвращает сторону, противоположную nSide.
function sideFlip( nSide )
{
	return 1 - nSide;
}

//Функция возвращает true если все лунки на стороне nSide пусты.
function isEmpty(nSide)
{
	return [...document.querySelectorAll(getStrSide( nSide ))].every(cell => {
		return cell.innerHTML == '0';
		});
}

//Сколько камней в лунке с данным ID?
function numberInID(strID)
{
		return Number(document.getElementById(strID).innerHTML);
}

// Функция возвращает true если игра закончена.
// Параметр: nSide - сторона следующего хода.
function endGame(nSide)
{
	// Если сторона с которой надо сделать ход пуста...
	if( isEmpty(nSide) )
	{
		var nInKalakh = numberInID(getKalakh(sideFlip(nSide))); 
		
		//Переносим все камни с противолежащей стороны в соответствующий калах.
		document.querySelectorAll(getStrSide(sideFlip(nSide))).forEach(the_well => {
			nInKalakh += Number(the_well.innerHTML);
			the_well.innerHTML = 0;
		});

		document.getElementById(getKalakh(sideFlip(nSide))).innerHTML = nInKalakh;
	}
	else
		if( !(numberInID("6") > 36 || numberInID("13") > 36) )
			return false;

	if( numberInID("6") - numberInID("13") > 0 )
		setMessage("You Won!");
	else
		if( numberInID("6") - numberInID("13") < 0 )
			setMessage("You Lost!");
		else
			setMessage("It is Draw!");
	
	return true;
}		


function setMessage(message)
{
	document.getElementById('info').innerHTML = message;
}

//Задержка выполнения программы на ms миллисекунд.
function sleep(ms) {
	return new Promise(
		resolve => setTimeout(resolve, ms)
	);
}

function executeLevel(nInitialLevel = 3)
{
	const stars = [...document.querySelectorAll('[class^="level__star"]')];
	const result = document.querySelector(".level__result");

	for (var i=0; i < 5; ++i) 
		stars[i].innerHTML = i < nInitialLevel ? '\u2605' : '\u2606';
	
	printLevelResult(result, nInitialLevel);

  	stars.map(star => {
    		star.onclick = () => {
      			nLevel = stars.indexOf(star)+1;
            		printLevelResult(result, nLevel);
        		for (var i=0; i < 5; ++i) 
				stars[i].innerHTML = i < nLevel ? '\u2605' : '\u2606';
        	}
  	});
}

function printLevelResult(result, num = 0) {
	result.textContent = `${num}/5`;
}

