# Arvore_derivacao
Para testar exemplos diferentes mude o valor da variavel teste.
Exemplo de input:
c = 0
FUNCTION teste(): 
c = 5;
FUNCTION teste2():
c = 10;
Como output a arvore de derivação é gerada:
Árvore de derivação:
 name: program
children:
- name: expression
  children:
  - name: assignment_expression
    children:
    - name: ID
      value:
        value: c
    - name: IGUAL
      value:
        value: '='
    - name: value_expr
      children:
      - name: NUM
        value:
          value: 0
- name: other_expression
  children:
  - name: expression
    children:
    - name: function
      children:
      - name: ID
        value:
          value: teste
      - name: LPAR
        value:
          value: (
      - name: RPAR
        value:
          value: )
      - name: DOISPONTOS
        value:
          value: ':'
      - name: other_expression
        value:
          value:
            name: other_expression
            children:
            - name: expression
              children:
              - name: assignment_expression
                children:
                - name: ID
                  value:
                    value: c
                - name: IGUAL
                  value:
                    value: '='
                - name: value_expr
                  children:
                  - name: NUM
                    value:
                      value: 5
  - name: other_expression
    children:
    - name: expression
      children:
      - name: function
        children:
        - name: ID
          value:
            value: teste2
        - name: LPAR
          value:
            value: (
        - name: RPAR
          value:
            value: )
        - name: DOISPONTOS
          value:
            value: ':'
        - name: other_expression
          value:
            value:
              name: other_expression
              children:
              - name: expression
                children:
                - name: assignment_expression
                  children:
                  - name: ID
                    value:
                      value: c
                  - name: IGUAL
                    value:
                      value: '='
                  - name: value_expr
                    children:
                    - name: NUM
                      value:
                        value: 10



