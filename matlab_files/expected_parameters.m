function boitesTolerance = expected_parameters(valeursNominales, alpha, nbSimulations)
  
  

    plagesTolerance = structfun(@(valeur) [valeur * (1 - alpha), valeur * (1 + alpha)], valeursNominales, 'UniformOutput', false);

   
   
    coefficients = struct('A0', zeros(1, nbSimulations), 'A1', zeros(1, nbSimulations), 'A2', zeros(1, nbSimulations), 'B0', zeros(1, nbSimulations), 'B1', zeros(1, nbSimulations));


    for i = 1:nbSimulations
        % Générer des paramètres aléatoires dans les plages de tolérance
        paramsAleatoires = structfun(@(tolerance) (tolerance(1) + (tolerance(2) - tolerance(1)) * rand), plagesTolerance, 'UniformOutput', false);
        R = paramsAleatoires.R;
        L = paramsAleatoires.L;
        C = paramsAleatoires.C;
        
        A0 = 1;
        A1 = R * C;
        A2 = L * C;
        B0 = 0;
        B1 = R * C;
        
        coefficients.A0(i) = A0;
        coefficients.A1(i) = A1;
        coefficients.A2(i) = A2;
        coefficients.B0(i) = B0;
        coefficients.B1(i) = B1;
    end

  
    boitesTolerance = structfun(@(valeurs) [min(valeurs), max(valeurs)], coefficients, 'UniformOutput', false);
    disp("Parameter range :");
    disp(boitesTolerance);
end
