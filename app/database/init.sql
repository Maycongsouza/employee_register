-- Trigger na tabela EMPLOYEE para tornar um colaborador líder de um departamento
CREATE OR REPLACE FUNCTION enforce_leadership_rules()
RETURNS TRIGGER AS $$
BEGIN
    -- Verifica se o cargo é de liderança
    IF (SELECT is_leadership FROM job WHERE id = NEW.job_id) THEN
        -- Impede que mais de um colaborador tenha o mesmo cargo de liderança
        IF EXISTS (
            SELECT 1 FROM employee
            WHERE job_id = NEW.job_id AND id != NEW.id
        ) THEN
            RAISE EXCEPTION 'O cargo de liderança já está ocupado.';
        END IF;

        -- Atualiza o líder do departamento e o campo is_leader
        UPDATE department SET leader_id = NEW.id WHERE id = NEW.department_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER enforce_leadership_trigger
AFTER INSERT OR UPDATE OF job_id ON employee
FOR EACH ROW
EXECUTE FUNCTION enforce_leadership_rules();

-- Trigger na tabela DEPARMENT para para atualizar o campo is_leader na tabela employee
CREATE OR REPLACE FUNCTION sync_is_leader()
RETURNS TRIGGER AS $$
BEGIN
    -- Marca como líder o funcionário associado ao leader_id
    UPDATE employee
    SET is_leader = (id = NEW.leader_id)
    WHERE department_id = NEW.id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER sync_is_leader
AFTER UPDATE OF leader_id ON department
FOR EACH ROW EXECUTE FUNCTION sync_is_leader();
