(function() {

    // 定数
    const field_width = 5;
    const field_height = 5;
    const cards = ("ABCDEFGHIJKL".repeat(2) + "X").split("");
    const gameset_count = 24;

    // 要素
    var divs = [];
    var button = document.createElement("div");
    var score = document.createElement("div");

    // 1, 2枚目のオープン（番号）
    var first = -1;
    var second = -1;
    // 揃ったかどうか
    var confirm_array = [];

    // やり直し回数
    var count = 0;
    // クリアかどうか
    var cleared = false;

    // ランダムな並び替え
    function shuffle(array) {
        for (var i = array.length - 1; i > 0; i--) {
            var t = Math.floor(Math.random() * (i + 1));
            tmp = array[i];
            array[i] = array[t];
            array[t] = tmp;
        }
    }

    // 子要素を排除
    function clear(obj) {
        while (obj.firstChild) {
            obj.removeChild(obj.firstChild);
        }
    }

    // ボード初期化
    function initialize() {
        var game = document.getElementById("game");

        clear(game);
        shuffle(cards);

        for (var i = 0; i < field_height; i++) {
            for (var j = 0; j < field_width; j++) {
                var div = document.createElement("div");
                div.className = "card";
                div.style.top = String(i * 72) + "px";
                div.style.left = String(j * 72) + "px";
                game.appendChild(div);

                divs.push(div);

                (function() {
                    var new_i = i;
                    var new_j = j;

                    div.onclick = function() {
                        click(new_i, new_j);
                    };
                })();
            }
        }

        // やり直しボタンを配置
        button.className = "button";
        button.style.top = String(field_height * 72) + "px";
        button.innerHTML = "やり直し";
        button.onclick = reset;
        game.appendChild(button);

        // 点数
        score.className = "score";
        score.style.top = String(field_height * 72) + "px";
        score.style.left = "216px";
        score.innerHTML = "回数: 0";
        game.appendChild(score);
    }

    // カードクリック時の動作
    function click(i, j) {
        if (second != -1) {
            return;
        }

        var index = i * field_width + j;
        var div = divs[index];
        var card = cards[index];

        // カード内容の表示
        div.innerHTML = card;

        // 1枚目の場合
        if (first == -1) {
            first = index;
            div.classList.add("open");
        }
        // 2枚目の場合
        else {
            // 一致した場合
            if (cards[first] == card) {
                divs[first].classList.remove("open");
                divs[first].classList.add("confirm");
                div.classList.add("confirm");
                first = -1;
                second = -1;
            }
            // 違った場合
            else {
                second = index;
                div.classList.add("open");
            }
        }
    }

    // めくったカードをもとに戻す
    function reset() {
        if (first == -1 || second == -1) {
            return;
        }

        divs[first].classList.remove("open");
        divs[first].innerHTML = "";
        divs[second].classList.remove("open");
        divs[second].innerHTML = "";
        first = -1;
        second = -1;
        count += 1;

        scoring();
    }

    // 得点表示
    function scoring() {
        score.innerHTML = "回数: " + count;
    }

    // 読み込み完了時動作
    window.onload = function() {
        initialize();
    }

})();
