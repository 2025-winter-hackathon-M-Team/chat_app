/* チャンネル名、チャンネル説明を更新するモーダルの制御 */
'use strict';

// export const initUpdateChannelModal = () => {
    // 必要な情報をHTMLからJSに読み込む
    const buttonUpdateChannelOpen = document.getElementById('update-channel-modalOpen');
    const updateChannelModal = document.getElementById('update-channel-modal');
    const buttonUpdateChannelClose = document.getElementById('update-channel-modalClose');
    
    // 「＋部屋を追加」ボタンをクリックれたときにモーダルを表示する
    buttonUpdateChannelOpen.addEventListener('click', modalOpen);
    function modalOpen() {
        updateChannelModal.style.display = 'block';
    }

    // 「cancel」ボタンをクリックされたときにモーダルを閉じる
    buttonUpdateChannelClose.addEventListener('click', modalClose);
    function modalClose(){
        updateChannelModal.style.display = 'none';
    }

    // モーダルの外側をクリックされたときにモーダルを閉じる
    addEventListener('click', outsideClose);
    function outsideClose(e) {
        if (e.target == updateChannelModal) {
            updateChannelModal.style.display = 'none';
        }
    }
// }
