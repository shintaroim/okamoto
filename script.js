// おかもっちゃん プロトタイプ共通スクリプト

document.addEventListener('DOMContentLoaded', () => {
    // スムーズスクロール
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // お問い合わせモーダル等の簡単なイベント
    const consultBtns = document.querySelectorAll('.btn-consult-trigger');
    consultBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            alert('【プロトタイプ動作】\nお問い合わせフォーム、または公式LINE相談画面が立ち上がります。\n（実機ではLINE友だち追加またはStudioフォームへ遷移します）');
        });
    });
});
