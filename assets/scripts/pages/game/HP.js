export class HP {
    actualHp = 0;

    hpContainer = undefined;

    hpEmptyElements = [];
    hpEmptyContainer = undefined;

    hpFullElements = [];
    hpFullContainer = undefined;

    createHpContainer() {
        this.hpContainer = document.createElement('div');
        this.hpContainer.classList = 'hp-container';

        this.hpContainer.appendChild(this.createHpEmptyElements());
        this.hpContainer.appendChild(this.createHpFullElements());

        return this.hpContainer;
    }
    
    createHpEmptyElements() {
        this.hpEmptyContainer = document.createElement('div');
        this.hpEmptyContainer.classList = 'hp-empty-container';
        
        for (let i = 0; i < 3; i++) {
            const hpEmptyElement = this.createHpEmptyElement();

            this.hpEmptyElements.push(hpEmptyElement);
            this.hpEmptyContainer.appendChild(hpEmptyElement);
        }
        
        return this.hpEmptyContainer;
    }

    createHpEmptyElement() {
        const hpEmptyElement = document.createElement('i');
        hpEmptyElement.classList = 'fa-regular fa-heart';

        return hpEmptyElement;
    }
    
    createHpFullElements() {
        this.hpFullContainer = document.createElement('div');
        this.hpFullContainer.classList = 'hp-full-container';

        for (let i = 0; i < 3; i++) {
            const hpFullElement = this.createHpFullElement();

            this.hpFullElements.push(hpFullElement);
            this.hpFullContainer.appendChild(hpFullElement);
        }

        return this.hpFullContainer;
    }

    createHpFullElement() {
        const hpFullElement = document.createElement('i');
        hpFullElement.classList = 'fa-solid fa-heart heart-full';

        return hpFullElement;
    }

    loseHp() {
        const hpElem = this.hpFullElements[this.actualHp - 1] ?? null;
        if (!hpElem) {
            return;
        }

        hpElem.style.transform = 'scale(0, 1)';
        this.actualHp -= 1;
    }

    addHp() {
        if (this.actualHp >= this.hpFullElements.length) {
            return;
        }

        const hpElem = this.hpFullElements[this.actualHp];
        hpElem.style.transform = 'scale(1, 1)';
        this.actualHp += 1
    }

    setActualHp(hp) {
        const actualHp = this.actualHp;
        const isIncrease = hp > actualHp;

        const iterationArray = [...Array( Math.abs(actualHp - hp))];

        for (const iter of iterationArray) {
            isIncrease ? this.addHp() : this.loseHp();
        }
    }
}