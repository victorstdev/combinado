let jogoData = null;
let selecionados = [];
let gruposResolvidos = [];
// Cores para os grupos resolvidos (Amarelo, Verde, Azul, Roxo)
const cores = ["#f48c06", "#226f54", "#00509d", "#5a189a"];

// 1. Carregar o JSON
// O parametro '?v=' evita que o navegador use cache velho
fetch('puzzle.json?v=' + new Date().getTime())
    .then(r => r.json())
    .then(data => {
        jogoData = data;
        document.getElementById('data-jogo').innerText = "Desafio de: " + data.data;
        iniciarJogo();
    })
    .catch(e => {
        document.getElementById('mensagem').innerText = "Erro ao carregar o jogo. Tente recarregar.";
        console.error(e);
    });

function iniciarJogo() {
    const tabuleiro = document.getElementById('tabuleiro');
    let todasPalavras = [];

    // Aplanar a estrutura para criar uma lista única de cartas
    jogoData.grupos.forEach((grupo, index) => {
        grupo.palavras.forEach(palavra => {
            todasPalavras.push({
                texto: palavra,
                grupoIndex: index, // Sabemos a qual grupo pertence
                id: Math.random().toString(36)
            });
        });
    });

    // Embaralhar (Algoritmo Fisher-Yates)
    for (let i = todasPalavras.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [todasPalavras[i], todasPalavras[j]] = [todasPalavras[j], todasPalavras[i]];
    }

    // Renderizar HTML
    todasPalavras.forEach(p => {
        const btn = document.createElement('div');
        btn.className = 'card';
        btn.innerText = p.texto;
        btn.dataset.grupo = p.grupoIndex; // Guardamos o segredo aqui (invisível pro usuário comum)
        btn.dataset.id = p.id;
        btn.onclick = () => selecionarCarta(btn);
        tabuleiro.appendChild(btn);
    });
}

let tentativas = 3;

function selecionarCarta(elemento) {
    // Se já está resolvido, ignora
    if (elemento.classList.contains('resolvido')) return;

    const id = elemento.dataset.id;

    // Se já selecionado, desmarca
    if (selecionados.includes(elemento)) {
        elemento.classList.remove('selecionado');
        selecionados = selecionados.filter(el => el !== elemento);
    } else {
        // Se não, marca
        elemento.classList.add('selecionado');
        selecionados.push(elemento);
    }

    // Habilita botão apenas se tiver 4
    document.getElementById('btn-verificar').disabled = selecionados.length !== 4;
}

function verificarGrupo() {
    if (selecionados.length !== 4) return;

    // Pega o índice do grupo da primeira carta
    const grupoAlvo = selecionados[0].dataset.grupo;

    // Verifica se TODAS as 4 cartas tem o mesmo índice
    const acertou = selecionados.every(el => el.dataset.grupo === grupoAlvo);

    if (acertou) {
        // EFEITO DE SUCESSO
        const infoGrupo = jogoData.grupos[grupoAlvo];
        const corGrupo = cores[gruposResolvidos.length % cores.length];

        // Remove as cartas do grid visual
        selecionados.forEach(el => el.style.display = 'none');

        // Cria a barra de grupo resolvido no topo
        const divResolvido = document.createElement('div');
        divResolvido.className = 'grupo-resolvido';
        divResolvido.style.backgroundColor = corGrupo;
        divResolvido.innerHTML = `<strong>${infoGrupo.tema}</strong><br><span>${infoGrupo.palavras.join(', ')}</span>`;

        // Insere antes do primeiro card
        const tabuleiro = document.getElementById('tabuleiro');
        tabuleiro.insertBefore(divResolvido, tabuleiro.firstChild);

        gruposResolvidos.push(grupoAlvo);
        selecionados = [];
        document.getElementById('btn-verificar').disabled = true;
        document.getElementById('mensagem').innerText = "Boa! Encontrou um grupo.";

        if (gruposResolvidos.length === 4) {
            document.getElementById('mensagem').innerText = "PARABÉNS! Você venceu!";
            document.getElementById('btn-verificar').style.display = 'none';
        }

    } else {
        // ERRO
        document.getElementById('mensagem').innerText = "Não é um grupo...";

        // Animaçãozinha simples (piscar)
        selecionados.forEach(el => {
            el.classList.add('erro');
            setTimeout(() => el.classList.remove('erro'), 500);
            // Opcional: Desmarcar tudo automaticamente ou deixar o usuário pensar?
            // Vamos desmarcar para forçar nova tentativa
            // el.classList.remove('selecionado');
        });
        // selecionados = []; // Se quiser limpar a seleção ao errar, descomente isso
    }
}