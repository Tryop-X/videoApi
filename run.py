from app import create_app
import os

# Obtén el puerto de la variable de entorno PORT o utiliza 5000 como valor predeterminado
port = int(os.environ.get('PORT', 5000))
app = create_app()
app.config['TIMEOUT'] = 480

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False)