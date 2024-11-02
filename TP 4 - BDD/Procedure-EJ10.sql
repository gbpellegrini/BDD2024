DELIMITER //
CREATE PROCEDURE C_AjustarPreciosCompetitivos ()
    BEGIN
    -- Declaracion de variables
        DECLARE V_ProductoId INT;
        DECLARE V_Precio DECIMAL(10,2);
        DECLARE V_Categoria VARCHAR(50);
        DECLARE V_PrecioPromedioCompetencia DECIMAL(10,2);
        DECLARE V_DiferenciaPrecio DECIMAL(10,2);

    -- Declaracion del cursor
    DECLARE C_PRODUCTOS CURSOR FOR
    SELECT P.ProductoId, P.Precio, P.Categoria
    FROM PRODUCTOS AS P

    BEGIN
        -- Declacion de una bandera de salia para el cursor
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
        --Apertura del cursor
        OPEN C_PRODUCTOS;

        --Obtencion de primer registro
        FETCH C_PRODUCTOS INTO V_ProductoId, V_Precio, V_Categoria;

        -- Iteacion para cada registro del cursor
        WHILE NOT done DO
            BEGIN
                -- Obtencion del precio promedio de la competencia
            SELECT V_PrecioPromedioCompetencia = AVG(PrecioCompetencia)
            FROM COMPRETENCIA_PRECIOS
            WHERE Categoria = V_Categoria;

            -- Continuar con otro producto si el actual no tiene precio
            IF V_PrecioPromedioCompetencia IS NULL
            BEGIN
                FETCH NEXT C_PRODUCTOS INTO V_ProductoId, V_Precio, V_Categoria;
                CONTINUE;
            END IF;
                
                -- Calcula la diferencia entre el precio actual y el precio promedio de la competencia
            SET V_DiferenciaPrecio = (V_Precio - V_PrecioPromedioCompetencia) / V_PrecioPromedioCompetencia;

            -- Ajustar precio dependiendo de la diferencia entre ambas companias
            IF V_DiferenciaPrecio > 5 THEN
                SET V_Precio = V_Precio * 0.95
                UPDATE PRODUCTOS
                SET Precio = V_Precio
                WHERE ProductoId = V_ProductoId;
            END IF;
            ELSE IF V_DiferenciaPrecio < -5 THEN
                SET V_Precio = V_Precio * 1.05
                UPDATE PRODUCTOS
                SET Precio = V_Precio
                WHERE ProductoId = V_ProductoId;
            END IF;

                -- Obtencion del sigueinte registro
                FETCH NEXT C_PRODUCTOS INTO V_ProductoId, V_Precio, V_Categoria;
        END;

    --Cierre del cursor y la liberacion de los recursos
    CLOSE C_PRODUCTOS;
    DEALLOCATE C_PRODUCTOS
    END //
DELIMITER;