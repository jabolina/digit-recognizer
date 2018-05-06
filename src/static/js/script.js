function documentReady(f) {
    let ready = setInterval(function () {
        if (document.readyState.indexOf('complete') > -1 || document.readyState.indexOf('interactive') > -1) {
            window.clearInterval(ready);
            f();
        }
    });
}

documentReady(function () {
    getRequest(window.location.href + 'already-trained', false, function (res) {
        (res.trained) ? document.querySelector('#predict-items').style.display = 'block' :
            document.querySelector('#predict-items').style.display = 'none';
    });

    document.querySelector('#train-button').addEventListener('click', function () {
        document.querySelector('#train-loader').style.display = 'block';
        let modelConf = {
            usePca: document.querySelector('#use-pca').checked,
            nbComponents: (document.querySelector('#use-pca').checked) ?
                document.querySelector('#pca-nb-components').value :
                -1,
            epochs: !!document.querySelector('#nb-epochs').value ? document.querySelector('#nb-epochs').value : -1
        };
        postRequest(window.location.href + 'train-model', modelConf, true, () => {
            document.querySelector('#train-loader').style.display = 'none';
            document.querySelector('#predict-items').style.display = 'block';
        });
    });

    document.querySelector('#use-pca').addEventListener('change', function () {
        document.querySelector('#pca-nb-components').disabled = !this.checked;
    });

    document.querySelector('#predict-button').addEventListener('click', function () {
        let index = document.querySelector('#predict-index').value;

        if (!!index) {
            if (index > 0 && index < 28000) {
                document.querySelector('#predict-loader').style.display = 'block';
                getRequest(window.location.href + 'predict/' + index, true, function (res) {
                    document.querySelector('#predict-loader').style.display = 'none';

                    let dots = res.image;
                    let canvas = document.getElementById('selected-image');
                    let ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.width);
                    for (let i=0; i<dots.length; i++) {
                        for (let j=0; j<dots[i].length; j++) {
                            if (dots[i][j] === 1) {
                                ctx.fillStyle = 'black';
                            } else {
                                ctx.fillStyle = 'white';
                            }
                            ctx.fillRect(i*10, j*5, 10, 5);
                        }
                    }
                    document.querySelector('#predicted-value').innerText = res.predicted;
                });
            } else {
                alert('Indice excedeu o intervalo disponivel!');
            }
        } else {
            alert('Indice da imagem precisa ser fornecido!');
        }
    });
});
