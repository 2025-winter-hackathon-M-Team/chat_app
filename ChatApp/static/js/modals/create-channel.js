/* 新しいチャンネルを作成するモーダルの制御 */
'use strict';


// 必要な情報をHTMLからJSに読み込む
const buttonCreateChannelOpen = document.getElementById('create-channel-modalOpen');
const createChannelModal = document.getElementById('create-channel-modal');
const buttonCreateChannelClose = document.getElementById('create-channel-modalClose');

// 「＋部屋を追加」ボタンをクリックれたときにモーダルを表示する
buttonCreateChannelOpen.addEventListener('click', modalOpen);
function modalOpen() {
    createChannelModal.style.display = 'block';
}

// 「cancel」ボタンをクリックされたときにモーダルを閉じる
buttonCreateChannelClose.addEventListener('click', modalClose);
function modalClose(){
    createChannelModal.style.display = 'none';
}

// モーダルの外側をクリックされたときにモーダルを閉じる
addEventListener('click', outsideClose);
function outsideClose(e) {
    if (e.target == createChannelModal) {
        createChannelModal.style.display = 'none';
    }
}