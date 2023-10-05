# wsFastAPItest

Requisitos: 
  fastapi y ponyorm
1. Exportar pythonpath
2. Levantar api
3. Abrir 0.0.0.0:8000/
4. Con postman crear una partida ej:
    0.0.0.0:8000/game/?game_name=partida&min_players=2&max_players=4
5. Crear un jugador:
    0.0.0.0:8000/player?player_name=pedro&game_id=1

Ahora en el navegador se vera la partida y su jugador.

Agregar otro jugador. 

Se actualizara la lista y los jugadores estan en orden por id

Solo escucha a los cambios en game1. 

