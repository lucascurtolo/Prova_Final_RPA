from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Cachorro(Base):
    __tablename__ = "cachorros"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    bred_for = Column(String)
    breed_group = Column(String)
    life_span = Column(String)
    temperament = Column(String)
    country_code = Column(String)
    height_metric = Column(String)
    weight_metric = Column(String)
    image_url = Column(String)

    dados_processados = relationship("DadosProcessados", back_populates="cachorro", uselist=False)

class DadosProcessados(Base):
    __tablename__ = "dados_processados"
    id = Column(Integer, primary_key=True)
    cachorro_id = Column(Integer, ForeignKey("cachorros.id"))
    temperament_count = Column(Integer)
    min_life_span = Column(Integer)
    max_life_span = Column(Integer)

    cachorro = relationship("Cachorro", back_populates="dados_processados")

engine = create_engine("sqlite:///projeto_rpa.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
