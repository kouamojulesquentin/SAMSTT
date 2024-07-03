function values_to_return = identify_oe_model(csv_file, nf, nb)
 
    data = readtable(csv_file);
    
   
    if ~all(ismember({'time', 'V_in', 'V_out'}, data.Properties.VariableNames))
        error('CSV file must contain columns: time, V_in, V_out');
    end


    time = data.time;
    V_in = data.V_in;
    V_out = data.V_out;


    data_id = iddata(V_in, V_out, mean(diff(time)));

    nk = 1; % Input delay

  
    model = oe(data_id, [nb nf nk]);
   transfer_function = tf(model);


    Numerators = transfer_function.Numerator{1, 1};
    Denominators = transfer_function.Denominator{1, 1};
    values_to_return = [Numerators, Denominators];
end
